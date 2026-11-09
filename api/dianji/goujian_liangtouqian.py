"""
构建《鬼谷子两头钳》数据 dianji/liangtouqian.json（只在维护数据时运行，线上不依赖本脚本）。

来源：古籍原文属公有领域。正文取自 enter.tw 逐格录入本（年干时干 100 格，每格一页）；
卦名、星名取自韩国朗月命理学堂（nangwol.com）录入的全本，并用它逐格比对「判断」以发现错挂、漏录（该本缺丁庚一格，另据 getit01 录入本补卦名、星名）。
处理：繁转简、修正录入错字；「判断」中含宿命断语的分句删去（以「……」标示），含禁用词的白话解与诗整条不收
（诗中「孤鸿」「夭桃」一类属意象，诗不以「孤」字过滤）。

    pip install opencc-python-reimplemented   # 仅构建时需要
    cd api && python -m dianji.goujian_liangtouqian [--huancun /tmp/ltq_cache]
"""
import argparse
import difflib
import html
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

from .goujian import FENJU, JINYONG_CI, guifan, xie_json

ZHENGWEN_URL = "https://enter.tw/{bianhao:03d}.htm"
JIAODUI_URL = "https://nangwol.com/post/4921"
USER_AGENT = "wtian-classics-builder/1.0 (https://github.com/timmy1688/wtian)"
MULU = Path(__file__).resolve().parent
LIANGTOUQIAN_WENJIAN = MULU / "liangtouqian.json"
QINGQIU_JIANGE = 0.5
XUKE = "古籍原文属公有领域；正文据 enter.tw 录入本，卦名、星名据韩国朗月命理学堂录入本，已繁转简并删去宿命断语。"

TIANGAN = "甲乙丙丁戊己庚辛壬癸"
YANG_ZHI = "子寅辰午申戌"
YIN_ZHI = "丑卯巳未酉亥"
LIUQIN = ["基业", "兄弟", "行藏", "婚姻", "子息", "收成"]
# Some transcriptions label 基业 as 基兴
LIUQIN_BIEMING = {"基兴": "基业"}
JIAODUI_XIANGSI_ZUIDI = 0.85
DIANHAO = re.compile(r"[，。；：！？、\s]")
# In the poems 孤 is imagery (孤鸿、孤雁) and 夭桃 is a peach blossom, not a verdict
SHIGE_JINYONG_CI = [ci for ci in JINYONG_CI if ci != "孤"]
SHIGE_YIXIANG = ["夭桃"]
# 丁庚 is missing from the second source; hexagram and stars from https://www.getit01.com/p201806092847331/
JIAODUI_BUCHONG = {"丁庚": {"gua": "临", "xing": ["天刚星", "天声星", "天灭星"], "panduan": ""}}


def shizhu_xulie(shigan: str) -> list:
    """时干所配的六个时柱：阳干配阳支，阴干配阴支。"""
    zhi = YANG_ZHI if TIANGAN.index(shigan) % 2 == 0 else YIN_ZHI
    return [shigan + z for z in zhi]


def zhua(url: str, wenjian: Path) -> str:
    if not wenjian.exists():
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            wenjian.write_bytes(response.read())
        time.sleep(QINGQIU_JIANGE)
    return wenjian.read_text(encoding="utf-8")


def chun_wen(fragment: str) -> str:
    """去 HTML 标签与零宽字符（录入本夹有 U+200B，会让引文逐字比对失败）。"""
    wen = html.unescape(re.sub(r"<[^>]+>", "", fragment))
    return re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", wen).strip()


def jiexi_zhengwen(yeman: str, jian: str) -> dict:
    """解析 enter.tw 一格：格诗、六时柱、判断、六亲诗。"""
    biaoti = re.search(r"年干時干</u>為\s*<font[^>]*>(..)</font>", yeman)
    if not biaoti or guifan(biaoti.group(1)) != jian:
        raise RuntimeError(f"{jian}: page title is {biaoti and biaoti.group(1)}")
    shi = re.search(r"<b>詩曰</b>\s*:(.*?)</p>", yeman, re.S)
    geming = re.search(r"<h2>(.+?)總評</h2>\s*<p>(.*?)</p>", yeman, re.S)
    shizhu = {
        guifan(chun_wen(zhu)): guifan(chun_wen(neirong))
        for zhu, neirong in re.findall(r"<p>時柱\s*<font[^>]*>(..)</font>\s*:(.*?)</p>", yeman, re.S)
    }
    liuqin = {}
    for xiang, neirong in re.findall(r"<p><b>(..)</b>\s*:(.*?)</p>", yeman, re.S):
        xiang = guifan(xiang)
        liuqin[LIUQIN_BIEMING.get(xiang, xiang)] = guifan(chun_wen(neirong))
    if not (shi and geming):
        raise RuntimeError(f"{jian}: poem or verdict not found")
    return {
        "geming": guifan(chun_wen(geming.group(1))),
        "geshi": guifan(chun_wen(shi.group(1))),
        "panduan": guifan(chun_wen(geming.group(2))),
        "shizhu": shizhu,
        "liuqin": liuqin,
    }


def jiexi_jiaodui(yeman: str) -> dict:
    """解析校对本：按「甲乙（恆）」分格，取卦名、按出现顺序的星名与判断。"""
    hang = [guifan(chun_wen(h)) for h in re.split(r"<br\s*/?>", yeman)]
    hang = [h for h in hang if h]
    jieguo, dangqian, deng_panduan = {}, None, False
    for neirong in hang:
        tou = re.fullmatch(rf"([{TIANGAN}])([{TIANGAN}])（(.{{1,3}})）", neirong)
        if tou:
            dangqian = jieguo.setdefault(tou.group(1) + tou.group(2), {"gua": tou.group(3), "xing": [], "panduan": ""})
            deng_panduan = False
            continue
        if dangqian is None:
            continue
        if re.fullmatch(r".{1,3}星[:：]?", neirong) and not dangqian["panduan"]:
            dangqian["xing"].append(neirong.rstrip(":："))
        elif neirong.startswith("判断"):
            deng_panduan = True
            yuxia = neirong[2:].lstrip(":：")
            if yuxia:
                dangqian["panduan"], deng_panduan = yuxia, False
        elif deng_panduan:
            dangqian["panduan"], deng_panduan = neirong, False
    return jieguo


def shanqu_duanyu(wen: str) -> tuple:
    """删去含禁用词的分句，连续删去处合为一个「……」。:return: (文字, 是否删改)"""
    baoliu, shanguo, gang_shan = [], False, False
    for fenju in FENJU.findall(wen):
        if any(ci in fenju for ci in JINYONG_CI):
            shanguo = True
            if not gang_shan:
                baoliu.append("……")
            gang_shan = True
            continue
        baoliu.append(fenju)
        gang_shan = False
    jieguo = "".join(baoliu)
    jieguo = re.sub(r"[，、；：]……", "……", jieguo)
    return jieguo, shanguo


def shige_ke_yong(shi: str) -> bool:
    for yixiang in SHIGE_YIXIANG:
        shi = shi.replace(yixiang, "")
    return not any(ci in shi for ci in SHIGE_JINYONG_CI)


def zhengli_ge(jian: str, zhengwen: dict, jiaodui: dict) -> tuple:
    """合并两本、过滤断语，返回 (格数据, 校对提示列表)。"""
    tishi = []
    xulie = shizhu_xulie(jian[1])
    if list(zhengwen["shizhu"]) != xulie:
        raise RuntimeError(f"{jian}: hour pillars {list(zhengwen['shizhu'])}, expected {xulie}")
    lost = [x for x in LIUQIN if x not in zhengwen["liuqin"]]
    if lost:
        raise RuntimeError(f"{jian}: missing {lost}")

    xing = jiaodui.get("xing", []) if len(jiaodui.get("xing", [])) == 3 else []
    if jiaodui.get("panduan"):
        xiangsi = difflib.SequenceMatcher(
            None, DIANHAO.sub("", zhengwen["panduan"]), DIANHAO.sub("", jiaodui["panduan"])).ratio()
        if xiangsi < JIAODUI_XIANGSI_ZUIDI:
            tishi.append(f"{jian}: verdict differs from the second source (similarity {xiangsi:.2f})")
        if not xing:
            tishi.append(f"{jian}: star names not parsed ({jiaodui.get('xing')})")
    elif not jiaodui:
        tishi.append(f"{jian}: absent from the second source, no hexagram or star names")

    shizhu = {}
    for xuhao, zhu in enumerate(xulie):
        pipei = re.fullmatch(r"(.+?)（解）(.*)", zhengwen["shizhu"][zhu])
        ming, jie = (pipei.group(1), pipei.group(2)) if pipei else (zhengwen["shizhu"][zhu], "")
        if any(ci in jie for ci in JINYONG_CI):
            jie = ""
        shizhu[zhu] = {"ming": ming, "jie": jie, "xing": xing[xuhao // 2] if xing else ""}

    panduan, shanguo = shanqu_duanyu(zhengwen["panduan"])
    liuqin = {x: zhengwen["liuqin"][x] for x in LIUQIN if shige_ke_yong(zhengwen["liuqin"][x])}
    geshi = zhengwen["geshi"] if shige_ke_yong(zhengwen["geshi"]) else ""
    return {
        "gua": jiaodui.get("gua", ""),
        "geming": zhengwen["geming"],
        "geshi": geshi,
        "panduan": panduan,
        "panduan_shanguo": shanguo,
        "shizhu": shizhu,
        "liuqin": liuqin,
    }, tishi


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--huancun", default="/tmp/ltq_cache", help="directory caching raw pages")
    huancun = Path(parser.parse_args().huancun)
    huancun.mkdir(parents=True, exist_ok=True)

    jiaodui_ben = jiexi_jiaodui(zhua(JIAODUI_URL, huancun / "nangwol_4921.html"))
    ge, tishi = {}, []
    for xuhao in range(100):
        jian = TIANGAN[xuhao // 10] + TIANGAN[xuhao % 10]
        bianhao = xuhao + 1
        yeman = zhua(ZHENGWEN_URL.format(bianhao=bianhao), huancun / f"enter_{bianhao:03d}.html")
        jiaodui = jiaodui_ben.get(jian) or JIAODUI_BUCHONG.get(jian, {})
        ge[jian], ge_tishi = zhengli_ge(jian, jiexi_zhengwen(yeman, jian), jiaodui)
        tishi += ge_tishi

    xie_json(LIANGTOUQIAN_WENJIAN, {
        "yuanxinxi": {
            "shuming": "鬼谷子两头钳", "bieming": ["鬼谷子分定经", "两头钳分定经"],
            "qufa": "年干配时干取格（共一百格），再按时柱取断语",
            "laiyuan": ["https://enter.tw/001.htm … 100.htm", JIAODUI_URL, "https://www.getit01.com/p201806092847331/"],
            "xuke": XUKE, "goujian_riqi": date.today().isoformat(),
            "guolv_ci": JINYONG_CI, "shige_guolv_ci": SHIGE_JINYONG_CI,
        },
        "ge": ge,
    })
    for item in tishi:
        print("  note:", item)
    shanguo = sum(g["panduan_shanguo"] for g in ge.values())
    shiqi = sum(len(LIUQIN) - len(g["liuqin"]) for g in ge.values())
    print(f"wrote {LIANGTOUQIAN_WENJIAN.name}: {len(ge)} entries; verdicts trimmed {shanguo}, poems dropped {shiqi}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

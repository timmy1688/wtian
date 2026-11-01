"""
构建八字典籍数据 dianji/ditiansui.json 与 dianji/qiongtong_baojian.json（只在维护数据时运行，线上不依赖本脚本）。

来源：维基文库录入的《滴天髓》（陈素庵辑要本，原文 + 旧注）与《穷通宝鉴》，古籍原文属公有领域。
处理：繁转简、修正录入错字、去掉例命表格；含宿命断语（寿夭、疾病、克夫克妻、贫贱、僧道等）的分句起截断不收，
《穷通宝鉴》另截去科甲、富贵一类的功名断语，只留调候用神。

    pip install opencc-python-reimplemented   # 仅构建时需要
    cd api && python -m dianji.goujian [--huancun /tmp/classics_cache]
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from opencc import OpenCC

WIKI_API = "https://zh.wikisource.org/w/api.php"
USER_AGENT = "wtian-classics-builder/1.0 (https://github.com/timmy1688/wtian)"
MULU = Path(__file__).resolve().parent
DITIANSUI_WENJIAN = MULU / "ditiansui.json"
QIONGTONG_WENJIAN = MULU / "qiongtong_baojian.json"
DITIANSUI_PIANSHU = 42
QINGQIU_JIANGE = 1.0
XUKE = "古籍原文属公有领域；录入文本取自维基文库（CC BY-SA 4.0），已繁转简并截取。"

TIANGAN = "甲乙丙丁戊己庚辛壬癸"
JIJIE_YUEFEN = {"春": (1, 2, 3), "夏": (4, 5, 6), "秋": (7, 8, 9), "冬": (10, 11, 12)}
# Longest labels first so 「十一二月」 is not read as 「十一月」
YUEFEN_BIAOJI = [
    ("十一二月", (11, 12)), ("正二月", (1, 2)), ("五六月", (5, 6)), ("七八月", (7, 8)),
    ("十一月", (11,)), ("十二月", (12,)), ("十月", (10,)), ("正月", (1,)), ("二月", (2,)),
    ("三月", (3,)), ("四月", (4,)), ("五月", (5,)), ("六月", (6,)), ("七月", (7,)), ("八月", (8,)), ("九月", (9,)),
]
CUOZI_JIAOZHENG = {"逄": "逢", "郤": "却", "倣": "仿", "囍": "喜", "豋": "登", "隹": "佳", "祇": "只", "籐": "藤", "縢": "藤"}
# A clause containing any of these ends the excerpt: the app must not relay fatalistic verdicts
JINYONG_CI = [
    "夭", "寿", "必死", "早死", "死于", "善终", "男命", "女命", "不忠", "残疾", "瞽", "目疾", "疾病", "病凶", "僧道", "孤", "贫", "贱", "下格",
    "盗贼", "嫖", "赌", "破家", "克妻", "克夫", "刑妻", "刑夫", "无子", "不肖", "娼", "妓", "狱", "凶厄",
    "女必", "女则",
]
# 穷通宝鉴 only keeps the 调候 lead of each month; verdict clauses about rank and wealth start here
DUANYU_CI = [
    "科甲", "登科", "及第", "富", "贵", "常人", "平人", "秀才", "生员", "贡", "功名", "一榜", "金榜", "黄榜",
    "衣衿", "白丁", "儒林", "风水", "庸", "劳苦", "困苦", "清寒", "妻", "子早",
    "玉堂", "金马", "黄阁", "翰苑", "显达", "名臣", "黉门", "皂隶", "雁塔", "腰金", "桃洞", "桃浪", "采芹",
    "食饩", "游庠", "一品", "为官", "云程", "青云", "上命", "上格", "平常", "成名", "立业", "名显", "异途",
]
FENJU = re.compile(r"[^，。；：！？、]+[，。；：！？、]?")
JIJIE_SHANGXIAN = 150
YUEFEN_SHANGXIAN = 150
ZHU_SHANGXIAN = 200
JIEDUAN_ZUISHAO = 15

zhuanhuan = OpenCC("t2s")


def zhua_wikitext(biaoti: str, huancun: Path) -> str:
    wenjian = huancun / (urllib.parse.quote(biaoti, safe="") + ".json")
    if not wenjian.exists():
        query = urllib.parse.urlencode({
            "action": "parse", "page": biaoti, "prop": "wikitext", "format": "json", "formatversion": 2,
        })
        request = urllib.request.Request(f"{WIKI_API}?{query}", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=30) as response:
            wenjian.write_bytes(response.read())
        time.sleep(QINGQIU_JIANGE)
    payload = json.loads(wenjian.read_text(encoding="utf-8"))
    if "parse" not in payload:
        raise RuntimeError(f"wikisource returned no content for {biaoti}: {payload.get('error')}")
    return payload["parse"]["wikitext"]


def guifan(wen: str) -> str:
    """繁转简、校正录入错字、去空白。"""
    wen = zhuanhuan.convert(wen)
    for cuo, zheng in CUOZI_JIAOZHENG.items():
        wen = wen.replace(cuo, zheng)
    return re.sub(r"\s+", "", wen)


def qu_biaoji(wen: str) -> str:
    """去掉 wiki 表格、模板与 HTML 标签。"""
    wen = re.sub(r"\{\|.*?\|\}", "", wen, flags=re.S)
    wen = re.sub(r"\{\{color\|[^|]+\|", "", wen)
    wen = wen.replace("{{+|", "")
    wen = re.sub(r"\{\{[^{}]*\}\}", "", wen)
    wen = wen.replace("}}", "").replace("{{", "")
    wen = re.sub(r"<[^>]+>", "", wen)
    return wen


def zhaiqu(wen: str, shangxian: int, jiezhi_ci=JINYONG_CI) -> tuple:
    """
    按分句摘取：遇到含截止词的分句或超过上限即停止。
    :return: (摘取的文字, 是否被截断)
    """
    baoliu = ""
    for fenju in FENJU.findall(wen):
        if any(ci in fenju for ci in jiezhi_ci) or len(baoliu) + len(fenju) > shangxian:
            return baoliu.rstrip("，、；：") + ("……" if baoliu else ""), True
        baoliu += fenju
    return baoliu, False


def goujian_ditiansui(huancun: Path) -> dict:
    """每篇取「原文 + 旧注」：原文含禁用词的整条不收，旧注按分句摘取。"""
    pian = {}
    for xuhao in range(1, DITIANSUI_PIANSHU + 1):
        bianhao = f"{xuhao:02d}"
        wikitext = zhua_wikitext(f"滴天髓/{bianhao}", huancun)
        pianming = re.search(r"\{\{Novel\|滴天髓\|([^|]+)", wikitext)
        zhengwen = wikitext.split("<onlyinclude>", 1)[-1].split("</onlyinclude>", 1)[0]
        yuanshi = []
        for hang in zhengwen.splitlines():
            if "{{+|" in hang:
                yuanshi.append({"yuanwen": guifan(qu_biaoji(hang)), "zhu": []})
            elif hang.startswith(":") and yuanshi:
                zhu = guifan(qu_biaoji(hang.lstrip(":")))
                if zhu:
                    yuanshi[-1]["zhu"].append(zhu)
        tiao = []
        for item in yuanshi:
            yuanwen = item["yuanwen"]
            if not yuanwen or any(ci in yuanwen for ci in JINYONG_CI):
                continue
            zhu, jieduan = zhaiqu("".join(item["zhu"]), ZHU_SHANGXIAN)
            tiao.append({"yuanwen": yuanwen, "zhu": zhu, "jieduan": jieduan})
        pian[bianhao] = {"pianming": guifan(pianming.group(1)) if pianming else bianhao, "tiao": tiao}
    return pian


def yuefen_biaoji(duan: str):
    for biaoji, yuefen in YUEFEN_BIAOJI:
        if duan.startswith(biaoji):
            return biaoji, yuefen
    return None, ()


def goujian_qiongtong(huancun: Path) -> dict:
    """按「三春/三夏/三秋/三冬某干」分节，取季节总论首段与各月首段（调候要旨）。"""
    wikitext = qu_biaoji(zhua_wikitext("穷通宝鉴", huancun))
    # Bold month markers often sit mid-paragraph after a removed table; give each its own paragraph
    wikitext = re.sub(r"'''([^']{1,8})'''", lambda m: f"\n\n{m.group(1)}", wikitext)
    wikitext = wikitext.replace("'''", "")
    biaoti_hang = list(re.finditer(r"^(=+)\s*(.+?)\s*=+\s*$", wikitext, re.M))
    jiezhi_ci = JINYONG_CI + DUANYU_CI

    jieguo = {}
    for xuhao, hang in enumerate(biaoti_hang):
        biaoti = hang.group(2)
        pipei = re.fullmatch(r"三([春夏秋冬])([甲乙丙丁戊己庚辛壬癸])[木火土金水]", biaoti)
        if not pipei:
            continue
        jijie, gan = pipei.groups()
        wuxing = biaoti[-1]
        jiewei = biaoti_hang[xuhao + 1].start() if xuhao + 1 < len(biaoti_hang) else len(wikitext)
        duanluo = [guifan(d) for d in wikitext[hang.end():jiewei].split("\n\n")]
        duanluo = [d for d in duanluo if d]

        rigan = jieguo.setdefault(gan, {"jijie": {}, "yuefen": {}})
        zhuyao_yue = set()
        zonglun = None
        for duan in duanluo:
            biaoji, yuefen = yuefen_biaoji(duan)
            if not biaoji:
                if zonglun is None and not zhuyao_yue:
                    wen, jieduan = zhaiqu(duan, JIJIE_SHANGXIAN, jiezhi_ci)
                    if not jieduan or len(wen) >= JIEDUAN_ZUISHAO:
                        zonglun = {"biaoti": biaoti, "wen": wen, "jieduan": jieduan}
                continue
            # 「正月丙火……」 is the month's own section; 「正月用壬……」 is a passing remark in the season intro
            zhuyao = re.match(rf"{biaoji}(之)?{gan}", duan) is not None
            wen, jieduan = zhaiqu(duan, YUEFEN_SHANGXIAN, jiezhi_ci)
            if jieduan and len(wen) < JIEDUAN_ZUISHAO:
                continue
            for yue in yuefen:
                jian = str(yue)
                if jian in rigan["yuefen"] and (yue in zhuyao_yue or not zhuyao):
                    continue
                rigan["yuefen"][jian] = {"biaoti": f"{biaoji}{gan}{wuxing}", "wen": wen, "jieduan": jieduan}
                if zhuyao:
                    zhuyao_yue.add(yue)
        if zonglun:
            rigan["jijie"][jijie] = zonglun
    return jieguo


def jiancha(ditiansui: dict, qiongtong: dict) -> list:
    wenti = []
    if len(ditiansui) != DITIANSUI_PIANSHU:
        wenti.append(f"ditiansui chapters {len(ditiansui)}")
    tiangan = {t["yuanwen"][0] for t in ditiansui["02"]["tiao"]}
    if tiangan != set(TIANGAN):
        wenti.append(f"tiangan verses cover {sorted(tiangan)}")
    for gan in TIANGAN:
        rigan = qiongtong.get(gan)
        if not rigan:
            wenti.append(f"qiongtong missing {gan}")
            continue
        for jijie, yuefen in JIJIE_YUEFEN.items():
            if not rigan["jijie"].get(jijie) and not any(str(y) in rigan["yuefen"] for y in yuefen):
                wenti.append(f"qiongtong {gan} {jijie} has neither intro nor month text")
    return wenti


def xie_json(lujing: Path, shuju: dict):
    lujing.write_text(json.dumps(shuju, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--huancun", default="/tmp/classics_cache", help="directory caching raw wikitext")
    huancun = Path(parser.parse_args().huancun)
    huancun.mkdir(parents=True, exist_ok=True)

    ditiansui = goujian_ditiansui(huancun)
    qiongtong = goujian_qiongtong(huancun)
    wenti = jiancha(ditiansui, qiongtong)
    if wenti:
        print("build failed:", *wenti, sep="\n  ")
        return 1

    riqi = date.today().isoformat()
    xie_json(DITIANSUI_WENJIAN, {
        "yuanxinxi": {
            "shuming": "滴天髓", "banben": "陈素庵辑要本（原文与旧注）",
            "laiyuan": "https://zh.wikisource.org/wiki/滴天髓", "xuke": XUKE,
            "goujian_riqi": riqi, "guolv_ci": JINYONG_CI,
        },
        "pian": ditiansui,
    })
    xie_json(QIONGTONG_WENJIAN, {
        "yuanxinxi": {
            "shuming": "穷通宝鉴", "banben": "维基文库录入本",
            "laiyuan": "https://zh.wikisource.org/wiki/穷通宝鉴", "xuke": XUKE,
            "goujian_riqi": riqi, "guolv_ci": JINYONG_CI + DUANYU_CI,
        },
        "rigan": qiongtong,
    })
    tiaoshu = sum(len(p["tiao"]) for p in ditiansui.values())
    yueshu = sum(len(v["yuefen"]) for v in qiongtong.values())
    jishu = sum(len(v["jijie"]) for v in qiongtong.values())
    print(f"wrote {DITIANSUI_WENJIAN.name}: {tiaoshu} passages; {QIONGTONG_WENJIAN.name}: {jishu} season intros + {yueshu} month texts")
    return 0


if __name__ == "__main__":
    sys.exit(main())

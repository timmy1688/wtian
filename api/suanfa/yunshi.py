"""
大运与流年。
"""
from datetime import date, datetime, timedelta
from typing import Optional

from .guanxi import qiu_ganzhi_guanxi
from .jiben import qiu_changsheng, qiu_shishen
from .jichu import DIZHI_CANGGAN, NIAN_ZHU, RI_ZHU, YUE_ZHU, ZHU_MING, jiazi_xuhao, shi_yanggan, xuhao_jiazi
from .lifa import lichun_nian_ganzhi, xianglin_jie

DAYUN_BUSHU = 8
HUIGUI_NIAN_TIANSHU = 365.2422
# 起运：三天折合一年
SANTIAN_YINIAN = 3
# 公元 4 年为甲子年
JIAZI_JIYUAN_NIAN = 4


def pai_dayun(chusheng: datetime, sizhu: list, xingbie: str) -> dict:
    """
    阳年男命、阴年女命顺排，反之逆排；大运从月柱起依次进退一位。
    起运岁数 = 出生时刻到下一个（顺排）或上一个（逆排）「节」的天数 ÷ 3。
    """
    shunpai = shi_yanggan(sizhu[NIAN_ZHU][0]) == (xingbie == "boy")

    shang_ming, shang_shike, xia_ming, xia_shike = xianglin_jie(chusheng)
    jie_ming, jie_shike = (xia_ming, xia_shike) if shunpai else (shang_ming, shang_shike)
    xiangcha_tian = abs((jie_shike - chusheng).total_seconds()) / 86400
    qiyun_sui = xiangcha_tian / SANTIAN_YINIAN

    nian = int(qiyun_sui)
    yue_xiaoshu = (qiyun_sui - nian) * 12
    yue = int(yue_xiaoshu)
    tian = int(round((yue_xiaoshu - yue) * 30))
    qiyun_shike = chusheng + timedelta(days=qiyun_sui * HUIGUI_NIAN_TIANSHU)

    yuezhu_xuhao = jiazi_xuhao(sizhu[YUE_ZHU])
    fangxiang = 1 if shunpai else -1
    rigan = sizhu[RI_ZHU][0]
    bu = []
    for i in range(DAYUN_BUSHU):
        ganzhi = xuhao_jiazi(yuezhu_xuhao + fangxiang * (i + 1))
        qishi_nian = qiyun_shike.year + 10 * i
        bu.append({
            "ganzhi": ganzhi,
            "start_year": qishi_nian,
            "end_year": qishi_nian + 9,
            "start_age": qishi_nian - chusheng.year + 1,
            "gan_shishen": qiu_shishen(rigan, ganzhi[0]),
            "zhi_shishen": qiu_shishen(rigan, DIZHI_CANGGAN[ganzhi[1]][0]),
            "stage": qiu_changsheng(rigan, ganzhi[1]),
        })

    return {
        "direction": "顺排" if shunpai else "逆排",
        "reference_jie": jie_ming,
        "start_desc": f"出生后{nian}年{yue}个月{tian}天起运",
        "start_date": qiyun_shike.strftime("%Y-%m-%d"),
        "steps": bu,
    }


def cha_dangqian_dayun(dayun: Optional[dict], nian: int) -> Optional[dict]:
    if not dayun:
        return None
    for bu in dayun["steps"]:
        if bu["start_year"] <= nian <= bu["end_year"]:
            return bu
    return None


def pai_liunian(jinri: date, sizhu: list, dayun: Optional[dict], wanglai_nian: int = 1) -> list:
    """当年及后续流年（以立春换年），附十神与对原局、大运的作用关系。"""
    rigan = sizhu[RI_ZHU][0]
    yuanju = [(f"{ZHU_MING[i]}柱", gz) for i, gz in enumerate(sizhu)]
    jinnian_xuhao = jiazi_xuhao(lichun_nian_ganzhi(jinri))
    # 立春前仍属上一干支年
    jinnian = jinri.year if (jinri.year - JIAZI_JIYUAN_NIAN) % 60 == jinnian_xuhao else jinri.year - 1

    jieguo = []
    for pianyi in range(wanglai_nian + 1):
        ganzhi = xuhao_jiazi(jinnian_xuhao + pianyi)
        nian = jinnian + pianyi
        ganzhi_lie = list(yuanju)
        dangqian = cha_dangqian_dayun(dayun, nian)
        if dangqian:
            ganzhi_lie.append(("大运", dangqian["ganzhi"]))
        ganzhi_lie.append(("流年", ganzhi))
        jieguo.append({
            "year": nian,
            "ganzhi": ganzhi,
            "gan_shishen": qiu_shishen(rigan, ganzhi[0]),
            "zhi_shishen": qiu_shishen(rigan, DIZHI_CANGGAN[ganzhi[1]][0]),
            "dayun": dangqian["ganzhi"] if dangqian else None,
            "relations": qiu_ganzhi_guanxi(ganzhi_lie, zhuti="流年"),
        })
    return jieguo

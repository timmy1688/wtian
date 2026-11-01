"""
汇总：由四柱（或出生时刻）生成完整命盘。返回字典的字段名是对外接口约定，保持不变。
"""
from datetime import date, datetime
from typing import Optional

from .guanxi import qiu_ganzhi_guanxi
from .jiben import qiu_changsheng, qiu_nayin, qiu_shishen, qiu_wangxiang, qiu_xunkong
from .jichu import (
    DIZHI_CANGGAN, DIZHI_WUXING, RI_ZHU, TIANGAN_WUXING, WUXING_SHUNXU, YUE_ZHU, ZHU_MING, shi_yanggan,
)
from .lifa import pai_sizhu
from .wangshuai import pan_wangshuai, qu_xiyong, suan_wuxing_liliang
from .yunshi import cha_dangqian_dayun, pai_dayun, pai_liunian


def biaomian_wuxing_zhanbi(sizhu: list) -> dict:
    """八字表面八个字的五行占比（百分比），供前端展示。"""
    geshu = {wx: 0 for wx in WUXING_SHUNXU}
    for ganzhi in sizhu:
        geshu[TIANGAN_WUXING[ganzhi[0]]] += 1
        geshu[DIZHI_WUXING[ganzhi[1]]] += 1
    zongshu = sum(geshu.values())
    return {wx: shu / zongshu * 100 for wx, shu in geshu.items()}


def sizhu_tiangan_shishen(sizhu: list) -> list:
    """四柱天干相对日主的十神，日柱本身为比肩（前端显示为日元）。"""
    rigan = sizhu[RI_ZHU][0]
    return [qiu_shishen(rigan, ganzhi[0]) for ganzhi in sizhu]


def _zhu_xiangqing(xuhao: int, ganzhi: str, rigan: str) -> dict:
    gan, zhi = ganzhi[0], ganzhi[1]
    canggan = DIZHI_CANGGAN[zhi]
    return {
        "label": ZHU_MING[xuhao],
        "ganzhi": ganzhi,
        "gan_shishen": "日主" if xuhao == RI_ZHU else qiu_shishen(rigan, gan),
        "zhi_shishen": qiu_shishen(rigan, canggan[0]),
        "hidden_gan": [{"gan": g, "wuxing": TIANGAN_WUXING[g], "shishen": qiu_shishen(rigan, g)} for g in canggan],
        "stage": qiu_changsheng(rigan, zhi),
        "nayin": qiu_nayin(ganzhi),
    }


def fenxi_sizhu(sizhu: list, xingbie: str, chusheng: Optional[datetime] = None,
                jinri: Optional[date] = None) -> dict:
    """基于四柱生成完整命盘。提供出生时刻时额外排大运；流年以 jinri 为基准。"""
    jinri = jinri or date.today()
    rigan = sizhu[RI_ZHU][0]
    xiangqing = [_zhu_xiangqing(i, gz, rigan) for i, gz in enumerate(sizhu)]

    shishen_tongji = {}
    for zhu in xiangqing:
        for mingcheng in (zhu["gan_shishen"], zhu["zhi_shishen"]):
            if mingcheng != "日主":
                shishen_tongji[mingcheng] = shishen_tongji.get(mingcheng, 0) + 1

    liliang = suan_wuxing_liliang(sizhu)
    wangshuai = pan_wangshuai(sizhu)
    biaomian = {wx: 0 for wx in WUXING_SHUNXU}
    for ganzhi in sizhu:
        biaomian[TIANGAN_WUXING[ganzhi[0]]] += 1
        biaomian[DIZHI_WUXING[ganzhi[1]]] += 1

    dayun = pai_dayun(chusheng, sizhu, xingbie) if chusheng else None

    return {
        "gender": "男" if xingbie == "boy" else "女",
        "day_master": {"gan": rigan, "wuxing": TIANGAN_WUXING[rigan], "yinyang": "阳" if shi_yanggan(rigan) else "阴"},
        "pillars": xiangqing,
        "shishen_count": shishen_tongji,
        "wuxing": {
            "surface_count": biaomian,
            "scores": liliang,
            "missing_surface": [k for k, v in biaomian.items() if v == 0],
            "missing_all": [k for k, v in liliang.items() if v == 0],
            "season_states": qiu_wangxiang(sizhu[YUE_ZHU][1]),
        },
        "strength": wangshuai,
        "favorable": qu_xiyong(rigan, wangshuai["level"], liliang),
        "xunkong": qiu_xunkong(sizhu[RI_ZHU]),
        "relations": qiu_ganzhi_guanxi([(f"{ZHU_MING[i]}柱", gz) for i, gz in enumerate(sizhu)]),
        "dayun": dayun,
        "current_dayun": cha_dangqian_dayun(dayun, jinri.year),
        "liunian": pai_liunian(jinri, sizhu, dayun),
        "today": jinri.isoformat(),
    }


def pai_mingpan(chusheng: datetime, xingbie: str, jinri: Optional[date] = None) -> dict:
    """由出生时刻排四柱并生成完整命盘（含大运）。"""
    mingpan = fenxi_sizhu(pai_sizhu(chusheng), xingbie, chusheng=chusheng, jinri=jinri)
    mingpan["birth_solar"] = chusheng.strftime("%Y-%m-%d %H:%M")
    return mingpan

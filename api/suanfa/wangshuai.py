"""
五行力量、日主旺衰（扶抑法）、喜用忌神。
"""
from .jiben import qiu_changsheng, qiu_wangxiang, qiu_wuxing
from .jichu import (
    CANGGAN_QUANZHONG, DIZHI_CANGGAN, KE_WO, RI_ZHU, SHENG_WO, TIANGAN_WUXING,
    WO_KE, WO_SHENG, WUXING_SHUNXU, YUE_ZHU, ZHU_MING,
)

YUELING_JIABEI = 2.0

# 同党占比阈值：低于阈值即取对应等级，均不低于则为身强
WANGSHUAI_DENGJI = [
    (0.28, "身弱"),
    (0.38, "偏弱"),
    (0.50, "中和"),
    (0.60, "偏强"),
]
SHENQIANG = "身强"
# 日主临这些长生位视为得令
DELING_CHANGSHENG = {"长生", "临官", "帝旺"}


def _canggan_fenzhi(zhi: str, quanzhong: float):
    canggan = DIZHI_CANGGAN[zhi]
    for gan, bili in zip(canggan, CANGGAN_QUANZHONG[len(canggan)]):
        yield gan, bili * quanzhong


def suan_wuxing_liliang(sizhu: list, han_rigan: bool = True) -> dict:
    """
    五行力量：天干每字计 1 分；地支按藏干权重拆分（1 藏干 1.0，2 藏干 0.7/0.3，3 藏干 0.6/0.3/0.1）；
    月支整体乘 2（月令加倍）。
    """
    fenshu = {wx: 0.0 for wx in WUXING_SHUNXU}
    for xuhao, ganzhi in enumerate(sizhu):
        if han_rigan or xuhao != RI_ZHU:
            fenshu[TIANGAN_WUXING[ganzhi[0]]] += 1.0
        quanzhong = YUELING_JIABEI if xuhao == YUE_ZHU else 1.0
        for gan, zhi_fen in _canggan_fenzhi(ganzhi[1], quanzhong):
            fenshu[TIANGAN_WUXING[gan]] += zhi_fen
    return {k: round(v, 2) for k, v in fenshu.items()}


def pan_wangshuai(sizhu: list) -> dict:
    """
    扶抑法初判日主强弱：同党（比劫 + 印）占全局五行力量（不含日干自身）的比例，按阈值分五级；
    另给出得令、得地（通根）、得势（天干帮扶）三项依据。
    """
    rigan = sizhu[RI_ZHU][0]
    ri_wuxing = TIANGAN_WUXING[rigan]
    tongdang = {ri_wuxing, qiu_wuxing(ri_wuxing, SHENG_WO)}

    fenshu = suan_wuxing_liliang(sizhu, han_rigan=False)
    zongfen = sum(fenshu.values())
    bili = sum(fenshu[wx] for wx in tongdang) / zongfen if zongfen else 0

    dengji = SHENQIANG
    for yuzhi, mingcheng in WANGSHUAI_DENGJI:
        if bili < yuzhi:
            dengji = mingcheng
            break

    yuezhi = sizhu[YUE_ZHU][1]
    yueling_benqi = TIANGAN_WUXING[DIZHI_CANGGAN[yuezhi][0]]
    deling = yueling_benqi in tongdang or qiu_changsheng(rigan, yuezhi) in DELING_CHANGSHENG

    dedi = [
        f"{ZHU_MING[xuhao]}支{ganzhi[1]}"
        for xuhao, ganzhi in enumerate(sizhu)
        if any(TIANGAN_WUXING[g] == ri_wuxing for g in DIZHI_CANGGAN[ganzhi[1]])
    ]
    deshi = [
        f"{ZHU_MING[xuhao]}干{ganzhi[0]}"
        for xuhao, ganzhi in enumerate(sizhu)
        if xuhao != RI_ZHU and TIANGAN_WUXING[ganzhi[0]] in tongdang
    ]

    return {
        "level": dengji,
        "support_ratio": round(bili, 3),
        "de_ling": deling,
        "de_di": dedi,
        "de_shi": deshi,
        "season_state": qiu_wangxiang(yuezhi)[ri_wuxing],
    }


def qu_xiyong(rigan: str, wangshuai_dengji: str, wuxing_liliang: dict) -> dict:
    """扶抑法取喜忌：身强喜克、泄、耗，身弱喜生、扶；中和取力量最弱一行以求流通。"""
    ri_wuxing = TIANGAN_WUXING[rigan]
    shengfu = [ri_wuxing, qiu_wuxing(ri_wuxing, SHENG_WO)]
    kexiehao = [qiu_wuxing(ri_wuxing, WO_SHENG), qiu_wuxing(ri_wuxing, WO_KE), qiu_wuxing(ri_wuxing, KE_WO)]
    if wangshuai_dengji in ("身强", "偏强"):
        return {"favorable": kexiehao, "unfavorable": shengfu, "note": "日主偏旺，宜克、泄、耗以求平衡"}
    if wangshuai_dengji in ("身弱", "偏弱"):
        return {"favorable": shengfu, "unfavorable": kexiehao, "note": "日主偏弱，宜生扶以求平衡"}
    zuiruo = min(wuxing_liliang, key=wuxing_liliang.get)
    return {"favorable": [zuiruo], "unfavorable": [], "note": "日主中和，以五行流通为美，可适度补益最弱之行"}

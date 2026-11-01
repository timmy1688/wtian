"""
基本推算：十神、十二长生、纳音、旬空、五行生克、月令旺相休囚死。
"""
from .jichu import (
    CHANGSHENG_QIDIAN, DIZHI, KE_WO, NAYIN, SHENG_WO, SHIER_CHANGSHENG, SHISHEN_BIAO,
    TIANGAN_WUXING, WO_KE, WO_SHENG, WUXING_SHUNXU, YUELING_WUXING, jiazi_xuhao, shi_yanggan,
)


def qiu_wuxing(jizhun: str, pianyi: int) -> str:
    """从基准五行沿相生方向数 pianyi 步：0 同我、1 我生、2 我克、3 克我、4 生我。"""
    return WUXING_SHUNXU[(WUXING_SHUNXU.index(jizhun) + pianyi) % 5]


def qiu_shishen(rigan: str, gan: str) -> str:
    """十神 = 生克关系（五行序差 mod 5）× 阴阳同异。"""
    pianyi = (WUXING_SHUNXU.index(TIANGAN_WUXING[gan]) - WUXING_SHUNXU.index(TIANGAN_WUXING[rigan])) % 5
    tongxing, yixing = SHISHEN_BIAO[pianyi]
    return tongxing if shi_yanggan(rigan) == shi_yanggan(gan) else yixing


def qiu_nayin(ganzhi: str) -> str:
    """六十甲子每两组共用一个纳音：纳音序 = 甲子序 // 2。"""
    return NAYIN[jiazi_xuhao(ganzhi) // 2]


def qiu_changsheng(gan: str, zhi: str) -> str:
    """十二长生：从该干长生之支起，阳干顺数、阴干逆数到目标地支。"""
    qidian = DIZHI.index(CHANGSHENG_QIDIAN[gan])
    mubiao = DIZHI.index(zhi)
    pianyi = (mubiao - qidian) % 12 if shi_yanggan(gan) else (qidian - mubiao) % 12
    return SHIER_CHANGSHENG[pianyi]


def qiu_xunkong(ganzhi: str) -> str:
    """旬空：一旬十干配十支，所余两支为空亡，即旬首地支之后第 10、11 位。"""
    xuhao = jiazi_xuhao(ganzhi)
    xunshou_zhi = (xuhao - xuhao % 10) % 12
    return DIZHI[(xunshou_zhi + 10) % 12] + DIZHI[(xunshou_zhi + 11) % 12]


def qiu_wangxiang(yuezhi: str) -> dict:
    """月令定五行旺相休囚死：当令者旺、我生者相、生我者休、克我者囚、我克者死。"""
    dangling = YUELING_WUXING[yuezhi]
    return {
        dangling: "旺",
        qiu_wuxing(dangling, WO_SHENG): "相",
        qiu_wuxing(dangling, SHENG_WO): "休",
        qiu_wuxing(dangling, KE_WO): "囚",
        qiu_wuxing(dangling, WO_KE): "死",
    }

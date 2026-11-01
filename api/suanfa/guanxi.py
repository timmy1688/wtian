"""
干支关系：天干五合与相冲，地支六合、六冲、相刑、自刑、相害，以及三合局、三会方。
"""
from itertools import combinations
from typing import Optional

from .jichu import (
    DIZHI_CHONG, DIZHI_HAI, DIZHI_LIUHE, DIZHI_SANHE, DIZHI_SANHUI, DIZHI_XING, DIZHI_ZIXING,
    TIANGAN_CHONG, TIANGAN_HE,
)


def qiu_ganzhi_guanxi(ganzhi_lie: list, zhuti: Optional[str] = None) -> list:
    """
    两两比对干支，列出合冲刑害；再看地支是否凑成三合（或含中神的半合）、三会。
    :param ganzhi_lie: [(标签, 干支)]，如 [("年柱", "甲子"), ...]
    :param zhuti: 只保留涉及该标签的关系（用于大运、流年对原局的作用）
    """
    jieguo = []
    for (la, a), (lb, b) in combinations(ganzhi_lie, 2):
        if zhuti and zhuti not in (la, lb):
            continue
        gan_dui = frozenset((a[0], b[0]))
        zhi_dui = frozenset((a[1], b[1]))
        if gan_dui in TIANGAN_HE:
            jieguo.append(f"{la}干{a[0]}与{lb}干{b[0]}相合（合化{TIANGAN_HE[gan_dui]}）")
        if gan_dui in TIANGAN_CHONG:
            jieguo.append(f"{la}干{a[0]}与{lb}干{b[0]}相冲")
        if zhi_dui in DIZHI_LIUHE:
            jieguo.append(f"{la}支{a[1]}与{lb}支{b[1]}六合（合{DIZHI_LIUHE[zhi_dui]}）")
        if zhi_dui in DIZHI_CHONG:
            jieguo.append(f"{la}支{a[1]}与{lb}支{b[1]}六冲")
        if zhi_dui in DIZHI_XING:
            jieguo.append(f"{la}支{a[1]}与{lb}支{b[1]}相刑")
        if a[1] == b[1] and a[1] in DIZHI_ZIXING:
            jieguo.append(f"{la}支{a[1]}与{lb}支{b[1]}自刑")
        if zhi_dui in DIZHI_HAI:
            jieguo.append(f"{la}支{a[1]}与{lb}支{b[1]}相害")

    xianyou_zhi = {ganzhi[1] for _, ganzhi in ganzhi_lie}
    zhuti_zhi = next((g[1] for l, g in ganzhi_lie if l == zhuti), None) if zhuti else None

    for sanzhi, zhongshen, wuxing in DIZHI_SANHE:
        chuxian = [z for z in sanzhi if z in xianyou_zhi]
        if zhuti_zhi and zhuti_zhi not in chuxian:
            continue
        if len(chuxian) == 3:
            jieguo.append(f"{sanzhi}三合{wuxing}局")
        elif len(chuxian) == 2 and zhongshen in chuxian:
            jieguo.append(f"{''.join(chuxian)}半合{wuxing}局")
    for sanzhi, wuxing in DIZHI_SANHUI:
        chuxian = [z for z in sanzhi if z in xianyou_zhi]
        if len(chuxian) == 3 and (not zhuti_zhi or zhuti_zhi in chuxian):
            jieguo.append(f"{sanzhi}三会{wuxing}方")
    return jieguo

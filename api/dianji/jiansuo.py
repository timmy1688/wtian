"""
八字典籍检索：按命盘特征确定性地选取《穷通宝鉴》《滴天髓》原文。

不用向量检索：日干、月令、强弱、冲合、关注方向本身就是精确的索引键，
同一命盘每次取到的原文相同，便于评测校验模型引用是否出自所给原文。
"""
from .ditiansui import cha_tiao, tiangan_lun
from .qiongtong import qu_tiaohou

# 月支 → 月序（寅月为正月）
YUEZHI_YUEXU = {"寅": 1, "卯": 2, "辰": 3, "巳": 4, "午": 5, "未": 6,
                "申": 7, "酉": 8, "戌": 9, "亥": 10, "子": 11, "丑": 12}

# 滴天髓条目以（篇号, 原文开头）定位
GUANZHU_TIAOMU = {
    "overall": [("34", "五行不戾")],
    "career": [("41", "何知其人贵")],
    "wealth": [("41", "何知其人富")],
    "love": [("34", "五行不戾")],
    "health": [("35", "五行和者")],
    "study": [("39", "清得静时")],
}
WANGSHUAI_TIAOMU = {
    "身强": ("12", "能知衰旺"), "偏强": ("12", "能知衰旺"),
    "身弱": ("12", "能知衰旺"), "偏弱": ("12", "能知衰旺"),
    "中和": ("13", "能识中和"),
}
HANNUAN_TIAOMU = ("16", "天道有寒暖")
HANNUAN_YUEZHI = set("亥子丑巳午未")
CHONG_TIAOMU = ("03", "支神只以冲为重")

ZONGZISHU_SHANGXIAN = 1100


def _you_dizhi_chong(guanxi: list) -> bool:
    return any("支" in item and "相冲" in item for item in guanxi)


def jiansuo_dianji(mingpan: dict, guanzhu: str) -> list:
    """
    按命盘选取典籍原文。顺序即优先级：调候 → 日干总论 → 关注方向 → 强弱 → 寒暖 → 冲。
    超出字数上限时从低优先级开始舍弃，前两段始终保留。
    :param guanzhu: 关注方向键，如 "career"
    :return: [{"chuchu": "穷通宝鉴·正月乙木", "wen": 原文, "zhu": 旧注或说明}]
    """
    rigan = mingpan["day_master"]["gan"]
    yuezhi = mingpan["pillars"][1]["ganzhi"][1]

    houxuan = [qu_tiaohou(rigan, YUEZHI_YUEXU[yuezhi]), tiangan_lun(rigan)]
    for tiaomu in GUANZHU_TIAOMU.get(guanzhu, GUANZHU_TIAOMU["overall"]):
        houxuan.append(cha_tiao(*tiaomu))
    wangshuai = WANGSHUAI_TIAOMU.get(mingpan["strength"]["level"])
    if wangshuai:
        houxuan.append(cha_tiao(*wangshuai))
    if yuezhi in HANNUAN_YUEZHI:
        houxuan.append(cha_tiao(*HANNUAN_TIAOMU))
    if _you_dizhi_chong(mingpan.get("relations", [])):
        houxuan.append(cha_tiao(*CHONG_TIAOMU))

    xuanzhong, yiyou, zishu = [], set(), 0
    for xuhao, duan in enumerate(houxuan):
        if not duan or duan["wen"] in yiyou:
            continue
        changdu = len(duan["wen"]) + len(duan["zhu"])
        if xuhao >= 2 and zishu + changdu > ZONGZISHU_SHANGXIAN:
            continue
        xuanzhong.append(duan)
        yiyou.add(duan["wen"])
        zishu += changdu
    return xuanzhong

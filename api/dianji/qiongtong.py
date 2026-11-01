"""
《穷通宝鉴》十干十二月调候。月份以寅月为正月（1）至丑月为十二月（12）。
"""
from functools import lru_cache
from typing import Optional

from . import du_json

YUEFEN_JIJIE = {1: "春", 2: "春", 3: "春", 4: "夏", 5: "夏", 6: "夏",
                7: "秋", 8: "秋", 9: "秋", 10: "冬", 11: "冬", 12: "冬"}
YUEFEN_HANZI = {1: "正", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六",
                7: "七", 8: "八", 9: "九", 10: "十", 11: "十一", 12: "十二"}


@lru_cache(maxsize=1)
def du_qiongtong() -> dict:
    return du_json("qiongtong_baojian.json")


def qu_tiaohou(rigan: str, yue: int) -> Optional[dict]:
    """
    取该日干在该月的调候段；原书未单列该月时退回季节总论，再退回同季最近月份并注明。
    :return: {"chuchu": "穷通宝鉴·正月乙木", "wen": 原文, "zhu": 说明}
    """
    shuju = du_qiongtong()["rigan"].get(rigan)
    if not shuju:
        return None
    benyue = shuju["yuefen"].get(str(yue))
    if benyue:
        return {"chuchu": f"穷通宝鉴·{benyue['biaoti']}", "wen": benyue["wen"], "zhu": ""}
    jijie = YUEFEN_JIJIE[yue]
    zonglun = shuju["jijie"].get(jijie)
    if zonglun:
        return {"chuchu": f"穷通宝鉴·{zonglun['biaoti']}", "wen": zonglun["wen"], "zhu": ""}
    tongji = [m for m in range(1, 13) if YUEFEN_JIJIE[m] == jijie and str(m) in shuju["yuefen"]]
    if not tongji:
        return None
    zuijin = shuju["yuefen"][str(min(tongji, key=lambda m: abs(m - yue)))]
    return {
        "chuchu": f"穷通宝鉴·{zuijin['biaoti']}",
        "wen": zuijin["wen"],
        "zhu": f"原书未单列{YUEFEN_HANZI[yue]}月，此为同季参照",
    }

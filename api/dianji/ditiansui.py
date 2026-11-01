"""
《滴天髓》原文与旧注。条目按（篇号, 原文开头）定位，数据重建后条目顺序变化也不会取错。
"""
from functools import lru_cache
from typing import Optional

from . import du_json

TIANGAN_LUN = "02"


@lru_cache(maxsize=1)
def du_ditiansui() -> dict:
    return du_json("ditiansui.json")


def _chuchu(pian: dict) -> str:
    """篇名本身含断语（如「贵贱贫富吉凶寿夭论」）时只标书名，避免把篇名当结论引用。"""
    guolv_ci = du_ditiansui()["yuanxinxi"]["guolv_ci"]
    return "滴天髓" if any(ci in pian["pianming"] for ci in guolv_ci) else f"滴天髓·{pian['pianming']}"


def cha_tiao(bianhao: str, kaitou: str) -> Optional[dict]:
    """
    :return: {"chuchu": "滴天髓·衰旺论", "wen": 原文, "zhu": 旧注}，找不到返回 None
    """
    pian = du_ditiansui()["pian"].get(bianhao)
    if not pian:
        return None
    for tiao in pian["tiao"]:
        if tiao["yuanwen"].startswith(kaitou):
            return {"chuchu": _chuchu(pian), "wen": tiao["yuanwen"], "zhu": tiao["zhu"]}
    return None


def tiangan_lun(rigan: str) -> Optional[dict]:
    """天干论中日干对应的一节（每节以该干开头）。"""
    return cha_tiao(TIANGAN_LUN, rigan)

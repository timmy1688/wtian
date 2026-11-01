"""
《周易》原文：卦辞、爻辞、大象、小象，按通行本卦序（1-64）索引。
"""
from functools import lru_cache

from . import du_json

QIAN_GUAXU = 1
KUN_GUAXU = 2


@lru_cache(maxsize=1)
def du_zhouyi() -> dict:
    shuju = du_json("zhouyi.json")
    if len(shuju) != 64:
        raise RuntimeError(f"zhouyi data is incomplete: {len(shuju)} hexagrams")
    return {int(k): v for k, v in shuju.items()}


def qu_gua(guaxu: int) -> dict:
    return du_zhouyi()[guaxu]

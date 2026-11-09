"""
《鬼谷子两头钳》：以年干、时干（四柱「两头」）取格，共一百格；每格再按时柱分六条断语。
"""
from functools import lru_cache
from typing import Optional

from . import du_json

# 关注方向 → 该格六亲诗中最相关的一首
GUANZHU_LIUQIN = {
    "overall": "收成",
    "career": "行藏",
    "wealth": "基业",
    "love": "婚姻",
    "health": "收成",
    "study": "行藏",
}


@lru_cache(maxsize=1)
def du_liangtouqian() -> dict:
    return du_json("liangtouqian.json")


def cha_ge(nian_gan: str, shizhu: str) -> Optional[dict]:
    """
    :param nian_gan: 年干，如 "丁"
    :param shizhu: 时柱干支，如 "庚子"
    :return: {"jian": "丁庚", "gua", "geming", "geshi", "panduan", "liuqin",
              "shizhu": "庚子", "shizhu_duan": {"ming", "jie", "xing"}}；干支无效返回 None
    """
    jian = nian_gan + shizhu[:1]
    ge = du_liangtouqian()["ge"].get(jian)
    if not ge or shizhu not in ge["shizhu"]:
        return None
    return {
        "jian": jian,
        "gua": ge["gua"],
        "geming": ge["geming"],
        "geshi": ge["geshi"],
        "panduan": ge["panduan"],
        "liuqin": ge["liuqin"],
        "shizhu": shizhu,
        "shizhu_duan": ge["shizhu"][shizhu],
    }


def liangtouqian_duan(nian_gan: str, shizhu: str, guanzhu: str) -> Optional[dict]:
    """
    供提示词引用的一段：格诗 + 判断 + 关注方向对应的六亲诗，时柱白话解作旧注。
    :return: {"chuchu": "鬼谷子两头钳·丁庚", "wen", "zhu", "fenduan": [(标签, 文字)], "biaoti": 格局说明}
    """
    ge = cha_ge(nian_gan, shizhu)
    if not ge:
        return None
    xiang = GUANZHU_LIUQIN.get(guanzhu, GUANZHU_LIUQIN["overall"])
    fenduan = [("格诗", ge["geshi"]), ("判断", ge["panduan"]), (xiang, ge["liuqin"].get(xiang, ""))]
    fenduan = [(biaoqian, wen) for biaoqian, wen in fenduan if wen]
    duan = ge["shizhu_duan"]
    return {
        "chuchu": f"鬼谷子两头钳·{ge['jian']}",
        "wen": "".join(wen for _, wen in fenduan),
        "zhu": duan["jie"],
        "fenduan": fenduan,
        "biaoti": f"年干{nian_gan}、时干{shizhu[0]}，{ge['gua']}卦，{ge['geming']}；"
                  f"时柱{shizhu}，{duan['xing']}「{duan['ming']}」",
    }

"""
动爻取用：按动爻数量决定以哪段经文为占断主体，依朱熹《易学启蒙·考变占》。
规则在此判定，经文原文从典籍层《周易》数据中取。
"""
from dianji.zhouyi import KUN_GUAXU, QIAN_GUAXU, qu_gua


def _yaoci(gua: dict, weizhi: int) -> dict:
    yao = gua["yao"][weizhi - 1]
    return {"chuchu": f"{gua['guaming']}·{yao['yaoming']}", "wen": yao["yaoci"], "xiang": yao["xiaoxiang"]}


def _guaci(gua: dict) -> dict:
    return {"chuchu": f"{gua['guaming']}·卦辞", "wen": gua["guaci"], "xiang": gua["daxiang"]}


def qu_jingwen(ben_guaxu: int, bian_guaxu: int, dongyao: list) -> dict:
    """
    :return: {"rule": 规则说明, "primary": [主断经文], "secondary": [辅参经文]}
    """
    ben = qu_gua(ben_guaxu)
    bian = qu_gua(bian_guaxu)
    dongyao = sorted(dongyao)
    jingyao = [p for p in range(1, 7) if p not in dongyao]
    dongshu = len(dongyao)

    if dongshu == 0:
        return {"rule": "六爻皆静，以本卦卦辞占", "primary": [_guaci(ben)], "secondary": []}
    if dongshu == 1:
        return {"rule": "一爻动，以本卦动爻爻辞占", "primary": [_yaoci(ben, dongyao[0])], "secondary": [_guaci(ben)]}
    if dongshu == 2:
        return {
            "rule": "二爻动，以本卦两动爻爻辞占，以上爻为主",
            "primary": [_yaoci(ben, dongyao[1])],
            "secondary": [_yaoci(ben, dongyao[0])],
        }
    if dongshu == 3:
        return {
            "rule": "三爻动，以本卦与变卦卦辞占，本卦为贞（主）、变卦为悔（辅）",
            "primary": [_guaci(ben)],
            "secondary": [_guaci(bian)],
        }
    if dongshu == 4:
        return {
            "rule": "四爻动，以变卦两静爻爻辞占，以下爻为主",
            "primary": [_yaoci(bian, jingyao[0])],
            "secondary": [_yaoci(bian, jingyao[1])],
        }
    if dongshu == 5:
        return {"rule": "五爻动，以变卦唯一静爻爻辞占", "primary": [_yaoci(bian, jingyao[0])], "secondary": [_guaci(bian)]}

    if ben_guaxu in (QIAN_GUAXU, KUN_GUAXU) and ben.get("yong"):
        yong = ben["yong"]
        return {
            "rule": f"六爻皆动，{ben['jianming']}卦以「{yong['yaoming']}」占",
            "primary": [{"chuchu": f"{ben['guaming']}·{yong['yaoming']}", "wen": yong["yaoci"], "xiang": yong["xiaoxiang"]}],
            "secondary": [_guaci(bian)],
        }
    return {"rule": "六爻皆动，以变卦卦辞占", "primary": [_guaci(bian)], "secondary": [_guaci(ben)]}

"""
把按日计数汇总成 /ops 页面要的数字、图和说明。

只处理已经聚合好的次数，不接触 Redis，也不出现生辰、问题或卦爻。
日期以调用方给出的「今天」为准，调用方负责换成上海时间。
"""
from datetime import date, timedelta

# 打开再拆成三页；详批再拆成八字和六爻。被挡住单独计，不进详批。
ZI_DUAN = {
    "home": "open_home",
    "bazi": "open_bazi",
    "gua": "open_gua",
}
JICHU_ZI = ("open_home", "open_bazi", "open_gua", "paipan", "qigua",
            "xiangpi_bazi", "xiangpi_gua", "blocked")
JIN_RI = 30
LIU_YUE = 6


def ye_mian_ziduan(page: str):
    """前端上报的页面名。不认识的名字返回 None，调用方不要计数。"""
    return ZI_DUAN.get(page)


def _hang(raw: dict, day: date) -> dict:
    row = {name: int(raw.get(name, 0) or 0) for name in JICHU_ZI}
    row["date"] = day.isoformat()
    row["open"] = row["open_home"] + row["open_bazi"] + row["open_gua"]
    row["xiangpi"] = row["xiangpi_bazi"] + row["xiangpi_gua"]
    return row


def _qu(store: dict, day: date) -> dict:
    return _hang(store.get(day.isoformat(), {}), day)


def _lianxu(store: dict, end: date, tianshu: int) -> list:
    """含 end 在内、往前 tianshu 天，按时间从早到晚。"""
    return [_qu(store, end - timedelta(days=tianshu - 1 - i)) for i in range(tianshu)]


def _yue_jia(day: date, yueshu: int) -> date:
    index = day.month - 1 + yueshu
    return date(day.year + index // 12, index % 12 + 1, 1)


def _yue_he(store: dict, start: date, end: date, today: date) -> dict:
    """[start, end) 这一个月的合计。end 可以晚于今天，多出来的日子是 0。"""
    he = {"open": 0, "paipan": 0, "qigua": 0, "xiangpi": 0}
    day = start
    last = min(end, today + timedelta(days=1))
    while day < last:
        row = _qu(store, day)
        for name in he:
            he[name] += row[name]
        day += timedelta(days=1)
    he["month"] = f"{start.year:04d}-{start.month:02d}"
    he["label"] = f"{start.month}月" if start.year == today.year else f"{start.year % 100}年{start.month}月"
    return he


def zengjian(dangqian: int, yiqian: int, jizhun: str) -> str:
    """「比昨天多 2」「与上月持平」这种短句。"""
    cha = dangqian - yiqian
    if cha > 0:
        return f"比{jizhun}多了 {cha}" if jizhun != "昨天" else f"比昨天多 {cha}"
    if cha < 0:
        return f"比{jizhun}少了 {-cha}" if jizhun != "昨天" else f"比昨天少 {-cha}"
    return f"与{jizhun}持平"


def _bili(blocked: int, xiangpi: int) -> str:
    he = blocked + xiangpi
    if he == 0:
        return "这三十日没有详批，也没有被挡住。"
    baifen = blocked * 100 / he
    wenzi = str(round(baifen)) if abs(baifen - round(baifen)) < 0.05 else f"{baifen:.1f}"
    return f"被挡住占详批与被挡住之和的 {wenzi}%。"


def huizong(store: dict, today: date) -> dict:
    """
    :param store: {"2026-11-14": {"open_home": 1, ...}}，缺的日子当 0
    :return: 页面直接用的结构。days 从早到晚，table 从今天往回排。
    """
    jin = _qu(store, today)
    zuo = _qu(store, today - timedelta(days=1))
    jinsanshi = _lianxu(store, today, JIN_RI)
    qiansanshi = _lianxu(store, today - timedelta(days=JIN_RI), JIN_RI)

    def heji(rows, name):
        return sum(row[name] for row in rows)

    xiangpi_jin = heji(jinsanshi, "xiangpi")
    xiangpi_qian = heji(qiansanshi, "xiangpi")
    blocked_jin = heji(jinsanshi, "blocked")

    chu = today.replace(day=1)
    yuefen = [_yue_he(store, _yue_jia(chu, i), _yue_jia(chu, i + 1), today) for i in range(-LIU_YUE + 1, 1)]
    benyue, shangyue = yuefen[-1], yuefen[-2]

    def kuai(key, label, parts=None):
        item = {
            "key": key,
            "label": label,
            "value": jin[key],
            "previous": zuo[key],
            "text": zengjian(jin[key], zuo[key], "昨天"),
        }
        if parts:
            item["parts"] = parts
        return item

    return {
        "today": today.isoformat(),
        "headline": [
            kuai("open", "打开", [
                {"label": "首页", "value": jin["open_home"]},
                {"label": "排盘页", "value": jin["open_bazi"]},
                {"label": "起卦页", "value": jin["open_gua"]},
            ]),
            kuai("paipan", "排盘"),
            kuai("qigua", "起卦"),
            kuai("xiangpi", "详批", [
                {"label": "八字", "value": jin["xiangpi_bazi"]},
                {"label": "六爻", "value": jin["xiangpi_gua"]},
            ]),
            kuai("blocked", "被挡住"),
        ],
        "days": [{name: row[name] for name in ("date", "open", "paipan", "qigua", "xiangpi", "blocked")}
                 for row in jinsanshi],
        "line_note": f"这三十日详批合计 {xiangpi_jin}，{zengjian(xiangpi_jin, xiangpi_qian, '再往前三十日')}。",
        "bar_note": _bili(blocked_jin, xiangpi_jin),
        "months": yuefen,
        "month_note": (
            f"本月打开{zengjian(benyue['open'], shangyue['open'], '上月')}，"
            f"详批{zengjian(benyue['xiangpi'], shangyue['xiangpi'], '上月')}。"
        ),
        "table": list(reversed(jinsanshi)),
    }

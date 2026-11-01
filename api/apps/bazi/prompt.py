"""
把程序推算的命盘渲染为提示词中的 <命盘> 数据块，并附上按命盘检索的 <典籍> 原文。
"""
from dianji.jiansuo import jiansuo_dianji

FOCUS_KEYS = {
    "综合运势": "overall",
    "事业": "career",
    "财运": "wealth",
    "感情": "love",
    "健康": "health",
    "学业": "study",
}
DEFAULT_FOCUS = "综合运势"


def normalize_focus(demand: str) -> str:
    demand = (demand or "").strip()
    return demand if demand in FOCUS_KEYS else DEFAULT_FOCUS


def _join(items: list, empty: str = "无") -> str:
    return "、".join(items) if items else empty


def _pillar_line(pillar: dict) -> str:
    hidden = "、".join(f"{h['gan']}{h['wuxing']}（{h['shishen']}）" for h in pillar["hidden_gan"])
    return (
        f"- {pillar['label']}柱 {pillar['ganzhi']}：天干{pillar['ganzhi'][0]}（{pillar['gan_shishen']}），"
        f"地支{pillar['ganzhi'][1]}（本气{pillar['zhi_shishen']}），藏干 {hidden}，"
        f"日主临此支为「{pillar['stage']}」，纳音{pillar['nayin']}"
    )


def _dayun_lines(chart: dict) -> list:
    dayun = chart.get("dayun")
    if not dayun:
        return ["大运：未提供出生时间，无法排大运，请只结合流年分析。"]
    lines = [
        f"大运（{dayun['direction']}，以{dayun['reference_jie']}起算，{dayun['start_desc']}，约 {dayun['start_date']} 交运）："
    ]
    for step in dayun["steps"]:
        lines.append(
            f"- {step['start_year']}-{step['end_year']}年（虚岁{step['start_age']}-{step['start_age'] + 9}岁）"
            f" {step['ganzhi']}：天干{step['gan_shishen']}，地支{step['zhi_shishen']}，日主临「{step['stage']}」"
        )
    current = chart.get("current_dayun")
    if current:
        lines.append(f"当前大运：{current['ganzhi']}（{current['start_year']}-{current['end_year']}年）")
    else:
        lines.append("当前大运：尚未起运")
    return lines


def render_chart(chart: dict) -> str:
    wuxing = chart["wuxing"]
    strength = chart["strength"]
    favorable = chart["favorable"]
    day_master = chart["day_master"]

    scores = "、".join(f"{k}{v}" for k, v in wuxing["scores"].items())
    surface = "、".join(f"{k}{v}" for k, v in wuxing["surface_count"].items())
    seasons = "、".join(f"{k}{v}" for k, v in wuxing["season_states"].items())
    shishen = "、".join(f"{k}{v}" for k, v in sorted(chart["shishen_count"].items(), key=lambda kv: -kv[1]))

    lines = [
        "<命盘>",
        f"基本信息：{chart['gender']}命"
        + (f"，公历出生 {chart['birth_solar']}" if chart.get("birth_solar") else "")
        + f"，测算基准日 {chart['today']}",
        "四柱：",
        *[_pillar_line(p) for p in chart["pillars"]],
        f"日主：{day_master['gan']}{day_master['wuxing']}（{day_master['yinyang']}），在月令中处于「{strength['season_state']}」",
        f"日主强弱（程序按扶抑法估算）：{strength['level']}；同党（比劫与印）力量占比 {strength['support_ratio'] * 100:.0f}%；"
        f"得令：{'是' if strength['de_ling'] else '否'}；得地（通根）：{_join(strength['de_di'])}；得势（天干帮扶）：{_join(strength['de_shi'])}",
        f"喜用（扶抑法初判，未计调候与特殊格局）：喜{_join(favorable['favorable'])}，忌{_join(favorable['unfavorable'])}；{favorable['note']}",
        f"十神分布（天干与地支本气）：{shishen}",
        f"五行力量（含藏干，月令加倍）：{scores}",
        f"五行表面字数：{surface}；表面缺：{_join(wuxing['missing_surface'])}；含藏干仍缺：{_join(wuxing['missing_all'])}",
        f"月令五行旺衰：{seasons}",
        f"日柱旬空：{chart['xunkong']}",
        f"原局干支关系：{_join(chart['relations'], '无明显合冲刑害')}",
        *_dayun_lines(chart),
        "流年：",
    ]
    for item in chart["liunian"]:
        lines.append(
            f"- {item['year']}年 {item['ganzhi']}：天干{item['gan_shishen']}，地支{item['zhi_shishen']}；"
            f"作用关系：{_join(item['relations'], '与原局无明显合冲')}"
        )
    lines.append("</命盘>")
    return "\n".join(lines)


def render_classics(passages: list) -> str:
    if not passages:
        return ""
    lines = ["<典籍>"]
    for passage in passages:
        if passage["chuchu"].startswith("穷通宝鉴"):
            lines.append(f"- 《{passage['chuchu']}》：{passage['wen']}")
            if passage["zhu"]:
                lines.append(f"  按：{passage['zhu']}")
            continue
        lines.append(f"- 《{passage['chuchu']}》原文：{passage['wen']}")
        if passage["zhu"]:
            lines.append(f"- 《{passage['chuchu']}》旧注：{passage['zhu']}")
    lines.append("</典籍>")
    return "\n".join(lines)


def render_user_message(chart: dict, focus: str) -> str:
    passages = jiansuo_dianji(chart, FOCUS_KEYS.get(focus, "overall"))
    return "\n".join(filter(None, [
        render_chart(chart),
        render_classics(passages),
        "<求问>",
        f"关注方向：{focus}",
        "</求问>",
        "请依据以上命盘与典籍，按系统要求完成解读。",
    ]))

"""
把卦象与取用经文渲染为提示词中的 <卦象> 数据块。
"""
from dianji.zhouyi import qu_gua
from suanfa.quyong import qu_jingwen
from utils.prompting import sanitize_question

FOCUS_KEYS = {
    "事业": "career",
    "爱情": "love",
    "财运": "wealth",
    "健康": "health",
    "学业": "study",
    "其他": "other",
}
DEFAULT_FOCUS = "其他"

TRIGRAM_IMAGE = {
    "乾": "天", "坤": "地", "震": "雷", "巽": "风",
    "坎": "水", "离": "火", "艮": "山", "兑": "泽",
}
POSITION_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]


def normalize_focus(category: str) -> str:
    category = (category or "").strip()
    return category if category in FOCUS_KEYS else DEFAULT_FOCUS


def _gua_line(label: str, info: dict) -> list:
    gua = qu_gua(info["number"])
    lower, upper = info["xiagua"], info["shanggua"]
    return [
        f"{label}：第{gua['guaxu']}卦 {gua['guaming']}（下{lower}上{upper}，{TRIGRAM_IMAGE[lower]}在下、{TRIGRAM_IMAGE[upper]}在上）",
        f"{label}卦辞：{gua['guaci']}　《大象》：{gua['daxiang']}",
    ]


def _passage(item: dict) -> str:
    text = f"- {item['chuchu']}：「{item['wen']}」"
    if item.get("xiang"):
        text += f"　《象》：{item['xiang']}"
    return text


def render_hexagram(hexagram: dict) -> str:
    bengua, biangua = hexagram["bengua"], hexagram["biangua"]
    moving = bengua["dongyao"]
    reading = qu_jingwen(bengua["number"], biangua["number"], moving)

    lines = ["<卦象>", "起卦方式：三枚铜钱法", *_gua_line("本卦", bengua)]
    if moving:
        lines.append("动爻：" + "、".join(POSITION_NAMES[p - 1] for p in moving))
        lines.extend(_gua_line("变卦", biangua))
    else:
        lines.append("动爻：无（六爻安静，无变卦）")
    lines.append(f"取用规则：{reading['rule']}")
    lines.append("主断经文：")
    lines.extend(_passage(p) for p in reading["primary"])
    if reading["secondary"]:
        lines.append("辅参经文：")
        lines.extend(_passage(p) for p in reading["secondary"])
    lines.append("</卦象>")
    return "\n".join(lines)


def render_user_message(hexagram: dict, gender: str, focus: str, question: str) -> str:
    question = sanitize_question(question)
    return "\n".join([
        render_hexagram(hexagram),
        "<求问>",
        f"性别：{'女' if gender == 'girl' else '男'}",
        f"事项：{focus}",
        f"具体问题：{question or '未填写，请围绕事项作整体解读'}",
        "</求问>",
        "请依据以上卦象，按系统要求完成解读。",
    ])

"""
模块化提示词组装。

系统提示 = 通用规则 + 领域方法 + 本次关注模块，全部为静态文本，按固定顺序拼接，
使相同领域的请求共享前缀，命中 DeepSeek 的上下文缓存；用户数据只放在 HumanMessage 中。
"""
import re
from functools import lru_cache
from pathlib import Path

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"
QUESTION_MAX_LENGTH = 60
# Characters that could forge or close the XML-like data tags in the user message
TAG_CHARS = re.compile(r"[<>＜＞《》]")
WHITESPACE = re.compile(r"\s+")


@lru_cache(maxsize=64)
def load_prompt(relative_path: str) -> str:
    path = (PROMPT_DIR / relative_path).resolve()
    if PROMPT_DIR not in path.parents:
        raise ValueError(f"prompt path escapes prompt dir: {relative_path}")
    return path.read_text(encoding="utf-8").strip()


def build_system_prompt(domain: str, focus_key: str) -> str:
    return "\n\n".join([
        load_prompt("common/system.md"),
        load_prompt(f"{domain}/system.md"),
        "# 本次关注\n" + load_prompt(f"{domain}/focus/{focus_key}.md"),
    ])


def build_messages(domain: str, focus_key: str, user_content: str) -> list[BaseMessage]:
    return [
        SystemMessage(content=build_system_prompt(domain, focus_key)),
        HumanMessage(content=user_content),
    ]


def sanitize_question(text: str, max_length: int = QUESTION_MAX_LENGTH) -> str:
    """用户自由输入只作为数据：去掉可伪造标签的字符、压缩空白并截断。"""
    cleaned = TAG_CHARS.sub("", text or "")
    cleaned = WHITESPACE.sub(" ", cleaned).strip()
    return cleaned[:max_length]

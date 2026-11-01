"""
大模型流式输出（Server-Sent Events）。

事件格式为 `data: {json}\n\n`，type 取值：
- delta：增量文本 {"type": "delta", "text": "..."}
- done：正常结束 {"type": "done"}
- error：出错 {"type": "error", "message": "..."}
"""
import json
from typing import AsyncIterator

from fastapi.responses import StreamingResponse
from langchain_core.messages import BaseMessage

from utils.commom import chat, logger

SSE_HEADERS = {
    # no-transform stops intermediaries (dev-server compression, CDNs) from buffering chunks to compress them
    "Cache-Control": "no-cache, no-transform",
    # Disable nginx proxy buffering so chunks reach the browser immediately
    "X-Accel-Buffering": "no",
}


def _event(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


async def _stream_llm(messages: list[BaseMessage], tag: str) -> AsyncIterator[str]:
    total_chars = 0
    try:
        async for chunk in chat.astream(messages):
            text = chunk.content if isinstance(chunk.content, str) else ""
            if text:
                total_chars += len(text)
                yield _event({"type": "delta", "text": text})
        logger.info(f"llm stream finished tag={tag} chars={total_chars}")
        yield _event({"type": "done"})
    except Exception as exc:
        logger.exception(f"llm stream failed tag={tag}: {exc}")
        yield _event({"type": "error", "message": "AI 解读服务暂时不可用，请稍后再试"})


def sse_response(messages: list[BaseMessage], tag: str) -> StreamingResponse:
    return StreamingResponse(_stream_llm(messages, tag), media_type="text/event-stream", headers=SSE_HEADERS)

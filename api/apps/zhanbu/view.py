from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from suanfa.qigua import pai_gua, qi_gua
from utils.access_limit import check_ip_access
from utils.commom import chat, logger
from utils.prompting import build_messages
from utils.streaming import sse_response
from .prompt import FOCUS_KEYS, normalize_focus, render_user_message

app = APIRouter()

LEGACY_DEMAND_SEPARATORS = ("：", ":")


class AnalysisRequest(BaseModel):
    gender: str  # "boy" 或 "girl"
    hexagram_data: dict  # 卦象数据，仅采用 bengua.yao 与 bengua.dongyao，卦名由服务端重新推出
    category: Optional[str] = None  # 占卜事项，如 "事业"
    question: Optional[str] = None  # 具体问题（选填）
    demand: Optional[str] = None  # 兼容旧版前端："事项：具体问题"


def resolve_question(request: AnalysisRequest) -> tuple:
    if request.category:
        return normalize_focus(request.category), request.question or ""
    demand = (request.demand or "").strip()
    for sep in LEGACY_DEMAND_SEPARATORS:
        if sep in demand:
            category, question = demand.split(sep, 1)
            return normalize_focus(category), question
    return normalize_focus(demand), ""


def rebuild_hexagram(hexagram_data: dict) -> dict:
    try:
        bengua = hexagram_data["bengua"]
        return pai_gua([int(v) for v in bengua["yao"]], [int(p) for p in bengua.get("dongyao", [])])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=f"卦象数据不合法：{exc}")


def build_analysis_messages(request: AnalysisRequest, hexagram: dict) -> list:
    focus, question = resolve_question(request)
    content = render_user_message(hexagram, request.gender, focus, question)
    return build_messages("zhanbu", FOCUS_KEYS[focus], content)


# 起卦接口
@app.post("/zhanbu/cast_hexagram")
async def cast_hexagram():
    return {
        "status": "success",
        "hexagram_data": qi_gua()
    }


@app.post("/zhanbu/analyze_hexagram")
async def analyze_hexagram(request: AnalysisRequest, ip_check=Depends(check_ip_access)):
    logger.info(ip_check)
    if ip_check["status"] == "limited":
        return ip_check
    hexagram = rebuild_hexagram(request.hexagram_data)
    response = await chat.ainvoke(build_analysis_messages(request, hexagram))
    return {
        "status": "success",
        "gender": request.gender,
        "demand": request.demand,
        "gua": hexagram["bengua"]["gua"],
        "dongyao": hexagram["bengua"]["dongyao"],
        "biangua": hexagram["biangua"]["gua"],
        "result": response.content
    }


@app.post("/zhanbu/analyze_hexagram/stream")
async def analyze_hexagram_stream(request: AnalysisRequest, ip_check=Depends(check_ip_access)):
    logger.info(ip_check)
    if ip_check["status"] == "limited":
        return ip_check
    hexagram = rebuild_hexagram(request.hexagram_data)
    return sse_response(build_analysis_messages(request, hexagram), tag="zhanbu")

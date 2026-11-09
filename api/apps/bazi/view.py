from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from dianji.liangtouqian import cha_ge
from suanfa.lifa import ShengriCuowu, jiexi_shengri, nongli_miaoshu, pai_sizhu
from suanfa.mingpan import biaomian_wuxing_zhanbi, fenxi_sizhu, pai_mingpan, sizhu_tiangan_shishen
from utils.access_limit import check_ip_access
from utils.commom import chat, logger
from utils.prompting import build_messages
from utils.streaming import sse_response
from .prompt import FOCUS_KEYS, normalize_focus, render_user_message
from .schemas import FenxiRequest, PaipanRequest, PaipanResponse

app = APIRouter()


def paipan_jieguo(riqi_str: str, shi_nongli: bool, xingbie: str, shi_runyue: bool = False) -> dict:
    """排盘接口的返回内容：四柱、天干十神、表面五行占比、公农历描述、完整命盘与两头钳格局。"""
    chusheng = jiexi_shengri(riqi_str, shi_nongli, shi_runyue)
    sizhu = pai_sizhu(chusheng)
    return {
        "bazi": sizhu,
        "shishen": sizhu_tiangan_shishen(sizhu),
        "wuxing": biaomian_wuxing_zhanbi(sizhu),
        "new_birth": f"{chusheng.year}年{chusheng.month}月{chusheng.day}日{chusheng.hour}时",
        "old_birth": nongli_miaoshu(chusheng),
        "chart": fenxi_sizhu(sizhu, xingbie, chusheng=chusheng),
        "liangtouqian": cha_ge(sizhu[0][0], sizhu[3]),
    }


@app.post("/bazi/paipan", response_model=PaipanResponse)
async def paipan(request: PaipanRequest):
    try:
        jieguo = paipan_jieguo(request.birth, request.is_lunar, request.gender.value, request.is_leap_month)
    except ShengriCuowu as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"gender": request.gender, **jieguo}


def build_fenxi_messages(request: FenxiRequest) -> list:
    gender = request.gender.value
    if request.birth:
        try:
            chusheng = jiexi_shengri(request.birth, request.is_lunar, request.is_leap_month)
        except ShengriCuowu as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        mingpan = pai_mingpan(chusheng, gender)
    else:
        mingpan = fenxi_sizhu(request.bazi, gender)
    focus = normalize_focus(request.demand)
    return build_messages("bazi", FOCUS_KEYS[focus], render_user_message(mingpan, focus))


@app.post("/bazi/fenxi")
async def bazifenxi(request: FenxiRequest, ip_check=Depends(check_ip_access)):
    logger.info(ip_check)
    if ip_check["status"] == "limited":
        return ip_check
    response = await chat.ainvoke(build_fenxi_messages(request))
    return {
        "status": "success",
        "result": response.content
    }


@app.post("/bazi/fenxi/stream")
async def bazifenxi_stream(request: FenxiRequest, ip_check=Depends(check_ip_access)):
    logger.info(ip_check)
    if ip_check["status"] == "limited":
        return ip_check
    return sse_response(build_fenxi_messages(request), tag="bazi")

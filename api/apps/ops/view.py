"""
/ops 的两个接口。

上报只收页面名。汇总数字由外面的 nginx 限制来源，这里不做登录。
"""
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from pydantic import BaseModel

from utils.redis_tools import get_redis

from .jishu import ji, qu_huizong, ye_mian_ziduan

app = APIRouter()


class Fangwen(BaseModel):
    page: str


@app.post("/ops/visit", status_code=204)
async def visit(body: Fangwen):
    field = ye_mian_ziduan(body.page)
    if field is not None:
        await ji(field)
    return Response(status_code=204)


@app.get("/ops/stats")
async def stats(redis=Depends(get_redis)):
    return await qu_huizong(redis)

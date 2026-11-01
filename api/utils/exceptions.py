import os
from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from .logs import getLogger


logger = getLogger(os.environ.get('APP_NAME'))


def global_http_exception_handler(request: Request, exc):
    """
    全局HTTP请求处理异常
    :param request: HTTP请求对象
    :param exc: 本次发生的异常对象
    :return:
    """

    # 使用日志记录异常
    logger.error(f"发生异常：{exc.detail}")

    return JSONResponse({
        'code': exc.status_code,
        'err_msg': exc.detail,
        'status': 'Failed'
    })


def global_request_exception_handler(request: Request, exc):
    """
    全局请求校验异常处理函数
    :param request: HTTP请求对象
    :param exc: 本次发生的异常对象
    :return:
    """

    # Pydantic v2 puts the raised exception object into error["ctx"], which is not JSON serializable
    error = exc.errors()[0]
    err_msg = {
        'type': error.get('type'),
        'loc': list(error.get('loc', ())),
        'msg': error.get('msg'),
    }
    logger.warning(f"请求参数校验失败：{err_msg}")

    return JSONResponse({
        'code': status.HTTP_400_BAD_REQUEST,
        'err_msg': err_msg,
        'status': 'Failed'
    })
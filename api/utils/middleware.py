import os, time
from fastapi.responses import JSONResponse
from .logs import getLogger


async def log_requests(request, call_next):
    """
    日志中间件
    :param request: HTTP请求对象
    :param call_next: 下一步调用的中间件/视图函数
    :return:
    """
    logger = getLogger(os.environ.get('APP_NAME'))
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception as exc:
        # Must stay inside CORSMiddleware: a bare 500 without CORS headers is reported by browsers as a network error
        logger.exception(f"unhandled error path={request.url.path}: {exc}")
        response = JSONResponse(status_code=500, content={"status": "error", "message": "服务器内部错误，请稍后再试"})

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"path={request.url.path} timer={formatted_process_time}ms status_code={response.status_code}")

    return response
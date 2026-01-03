import os
from fastapi import FastAPI
from utils import middleware,exceptions,redis_tools
from fastapi.middleware.cors import CORSMiddleware
from apps.bazi.view import app as bazi_app
from apps.zhanbu.view import app as zhanbu_app



REDIS = {
    'host': os.environ.get('RD_HOST', '127.0.0.1'), # 数据库地址
    'port': os.environ.get('RD_PORT', 6379),        # 数据库端口
    'db': os.environ.get('RD_DB', 0),               # 数据库名
    'username':  os.environ.get('RD_USERNAME', ''), # 用户名
    'password':  os.environ.get('RD_PASSWORD', ''), # 密码
}

def create_app() -> FastAPI:
    """工厂函数：创建App对象"""
    # 读取环境配置文件的信息，加载到环境变量
    app = FastAPI(
        title="Twen",
        # 注册全局异常处理函数
        exception_handlers={
            exceptions.HTTPException: exceptions.global_http_exception_handler,
            exceptions.RequestValidationError: exceptions.global_request_exception_handler,
        }
    )


    #redis连接对象注册到App应用对象中
    redis_tools.register_redis(
        app,
        config=REDIS,
    )
    
    # 允许跨域的来源，可以设置为前端的 URL 地址
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8080",      # 本地开发
            "http://127.0.0.1:8080",      # 本地开发
            "http://127.0.0.1:8000",      # 本地开发
            "http://localhost:8000",      # 本地开发
            "http://192.168.100.101:8000",      # 本地开发       
            "https://wtian.cloud",        # HTTPS 域名
            "http://wtian.cloud",         # HTTP 域名（重定向用）
            "https://www.wtian.cloud",    # HTTPS www 域名
            "http://www.wtian.cloud",     # HTTP www 域名
            "https://47.107.237.220",     # HTTPS IP（如果直接访问）
            "http://47.107.237.220",      # HTTP IP
        ],  # 指定具体的域名，不能与 allow_credentials=True 同时使用通配符
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有 HTTP 方法
        allow_headers=["*"],  # 允许所有请求头
    )

    # 注册路由
    app.include_router(bazi_app)
    app.include_router(zhanbu_app)
    
    # 注册中间件函数
    http_middleware = app.middleware('http')
    http_middleware(middleware.log_requests)

    return app

app = create_app()

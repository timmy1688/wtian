export APP_NAME="wtian"
export WORKERS=4
export PORT=8000
export DASHSCOPE_API_KEY="xxxxxxxxx"
export RD_HOST="127.0.0.1"
export RD_PORT="16666"
export RD_DB=0
export RD_PASSWORD="123456"
export WHITELIST_IPS="127.0.0.1"
export ACCESS_LIMIT_PER_DAY=10
gunicorn -w $WORKERS -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
from langchain_openai import ChatOpenAI
from utils import logs
import os

logger = logs.getLogger(os.environ.get('APP_NAME'))

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
if not DEEPSEEK_API_KEY:
    raise RuntimeError("DEEPSEEK_API_KEY is not set, please configure it in api/.env or the environment")

DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
# DeepSeek v4 thinks before answering by default; "disabled" answers directly and much faster
DEEPSEEK_THINKING = os.environ.get("DEEPSEEK_THINKING", "disabled")

# 创建 ChatOpenAI 实例，通过 OpenAI 兼容协议调用 DeepSeek
chat = ChatOpenAI(
    model=DEEPSEEK_MODEL,
    openai_api_key=DEEPSEEK_API_KEY,
    openai_api_base=DEEPSEEK_BASE_URL,
    timeout=float(os.environ.get("DEEPSEEK_TIMEOUT", 110)),
    max_retries=2,
    extra_body={"thinking": {"type": DEEPSEEK_THINKING}},
)

from fastapi import APIRouter,Depends
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from utils.commom import logger,read_prompt,chat
from utils.access_limit import check_ip_access
from .zhanbu import generate_hexagram

app =APIRouter()





# 定义请求体的模型
class ZhanbuRequest(BaseModel):
    gender: str  # "boy" 或 "girl"
    demand: str  # 如 "问事业"

class AnalysisRequest(BaseModel):
    gender: str  # "boy" 或 "girl"
    demand: str  # 如 "问事业"
    hexagram_data: dict  # 卦象数据，包含 bengua 和 biangua 信息
    

# 起卦接口
@app.post("/zhanbu/cast_hexagram")
async def cast_hexagram():
    zhanbu = generate_hexagram()
    print(zhanbu)
    return {
        "status": "success",
        "hexagram_data": zhanbu
    }

@app.post("/zhanbu/analyze_hexagram")
async def analyze_hexagram(request: AnalysisRequest, ip_check=Depends(check_ip_access)):
    print("!!!!!!!!!!!!!!!!!!!")
    print(ip_check)
    if ip_check["status"] == "limited":
        return ip_check

    zhanbu = request.hexagram_data
    print(zhanbu)

    # 从文件读取提示词模板
    template = await read_prompt("prompts/zhanbu.txt")

    # 创建 PromptTemplate
    prompt = PromptTemplate(
        input_variables=["gender", "demand", "gua", "ben_xiagua", "ben_shanggua", "dongyao","biangua","bian_xiagua","bian_shangua"],
        template=template
    )

    # 填充模板
    input_prompt = prompt.format(
        gender=request.gender,
        demand=request.demand,
        gua=zhanbu["bengua"]["gua"],
        ben_xiagua=zhanbu["bengua"]["xiagua"],
        ben_shanggua=zhanbu["bengua"]["shanggua"],
        dongyao=zhanbu["bengua"]["dongyao"],
        biangua=zhanbu["biangua"]["gua"],
        bian_xiagua=zhanbu["biangua"]["xiagua"],
        bian_shangua=zhanbu["biangua"]["shanggua"]
    )

    # 定义消息
    messages = [
        HumanMessage(content=input_prompt),  # 使用填充后的提示词
    ]

    # 调用模型
    response = await chat.ainvoke(messages)

    # 打印响应内容（可选，用于调试）
    print(response.content)
    return {
        "status": "success",
        "gender": request.gender,
        "demand": request.demand,
        "gua": zhanbu["bengua"]["gua"],
        "dongyao": zhanbu["bengua"]["dongyao"],
        "biangua":zhanbu["biangua"]["gua"],
        "result": response.content
    }



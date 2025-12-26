# 问天AI (WenTian AI)

[![Stars](https://img.shields.io/github/stars/timmy1688/wtian?style=social)](https://github.com/timmy1688/wtian/stargazers)
[![Forks](https://img.shields.io/github/forks/timmy1688/wtian?style=social)](https://github.com/timmy1688/wtian/network/members)
[![License](https://img.shields.io/github/license/timmy1688/wtian)](LICENSE) <!-- 如果有LICENSE文件，请补充，否则删除这行 -->

一个将**大语言模型 (LLM)** 与**中国传统文化《周易》（I Ching）** 深度结合的AI问卦/解卦应用。

通过自然语言与AI对话，你可以像古代贤者一样“问天”——求卦、解卦、预测运势、人生建议，甚至结合现代事件进行周易解读。

## 🌟 项目特色

- 大模型驱动的智能解卦（支持多种LLM，如通义千问、ChatGPT、Claude 等）
- 传统周易算法 + AI 现代解读，兼顾经典与创新
- 支持起卦方式：手动输入、随机摇卦、报数起卦、时间起卦 等
- 完整的前后端分离架构，前端 Vue3 + Element Plus，后端 FastAPI + LangChain
- Docker 一键部署，轻松本地运行或云部署
- 支持多模型切换、历史记录、卦象可视化

## 🏗️ 软件架构

```
wtian/
├── api/          # FastAPI 后端代码（LangChain + LLM 调用）
├── ui/           # Vue3 前端代码（Vite + Element Plus）
├── docker/       # Docker Compose 配置
└── README.md
```

技术栈：
- 后端：Python 3.10+、FastAPI、LangChain、Pydantic
- 前端：Vue 3、Pinia、Vue Router、Element Plus
- 部署：Docker + Docker Compose
- LLM 支持：Qwen、通义千问、OpenAI、Claude、Gemini 等（通过 API Key 配置）

## 🚀 安装教程

### 方式一：Docker 部署（推荐）

```bash
# 克隆仓库
git clone https://github.com/timmy1688/wtian.git
cd wtian

# 复制环境变量示例文件并填写你的 API Key
cp .env.example .env
# 编辑 .env 文件，填写你的大模型 API Key（如 QWEN_API_KEY、OPENAI_API_KEY 等）

# 启动
docker-compose up -d
```

访问地址：http://localhost:8080 （前端）  
API 地址：http://localhost:8000

### 方式二：本地开发运行

#### 后端
```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 配置 .env 文件
cp .env.example .env

uvicorn main:app --reload --port 8000
```

#### 前端
```bash
cd ui
npm install
npm run dev
```

## 📖 使用说明

1. 打开网页，进入“问天”页面
2. 输入你的问题（如“明年事业运势如何？”）
3. 选择起卦方式（默认AI智能起卦）
4. AI 将自动为你起卦、变卦、解卦，并结合大模型给出深度解读
5. 支持导出卦象、保存历史记录

## 🤝 参与贡献

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feat/xxx`)
3. 提交你的改动 (`git commit -m 'feat: 添加 xxx 功能'`)
4. Push 到分支 (`git push origin feat/xxx`)
5. 打开 Pull Request

欢迎提交 Issue 或 PR，一起把周易与AI结合得更完美！

## 📄 许可证

[MIT License](LICENSE) （如无LICENSE文件，可自行选择开源协议）

---

**问天AI** —— 让千年智慧遇见现代AI，古为今用，问道未来。

如果觉得项目不错，欢迎点个 Star ✨ 支持一下！

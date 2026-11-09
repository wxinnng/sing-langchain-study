
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

# 加载 .env
load_dotenv()

# 读取环境变量
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL")

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    temperature=0,
    api_key=api_key,
    base_url=base_url,
    timeout=30,
    max_retries=1
)

# 发送消息
response = model.invoke(
    [
        HumanMessage(
            content="使用一句话总结一下，什么是 LangChain？"
        )
    ]
)

print(response.content)
print(type(response).__name__)

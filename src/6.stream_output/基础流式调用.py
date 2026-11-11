from provide_chat_model import get_chat_model_with_default_setting
import asyncio
from langchain.agents import create_agent
from langchain.messages import HumanMessage

model = get_chat_model_with_default_setting()


def based_use():

    for chunk in model.stream("给我讲个笑话"):

        # chunk是AIMessageChunk对象
        print(chunk.content, end = "", flush=True)

# based_use()

# 异步调用，在生产环境中，推荐使用
async def stream_response():
    async for chunk in model.astream('给我讲个笑话'):
        print(chunk.content, end="", flush=True)

# asyncio.run(stream_response())

# Agent下的流式调用
def agent_stream_output():

    # 创建Agent对象
    agent = create_agent(
        model=model,
        system_prompt='你是一个智能助手，请回答用户的问题'
    )

    for chunk in agent.stream(
        {
            'messages' : [HumanMessage('给我讲个笑话，别自己编，说个经典的')]
        },
        stream_mode='messages',  # messages模式
        version='v2'
    ):

        token, metadata = chunk['data']

        if token.content :

            # 流式打印
            print(token.content, end = '' , flush=True)

agent_stream_output()
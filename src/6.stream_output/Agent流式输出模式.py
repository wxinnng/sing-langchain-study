from provide_chat_model import get_chat_model_with_default_setting
import asyncio
from langchain.agents import create_agent
from langchain.messages import HumanMessage,AIMessageChunk
from langchain.tools import tool
from langgraph.config import get_stream_writer
import time

model = get_chat_model_with_default_setting()

@tool
def get_weather(city : str) -> str:
    """查询城市天气"""

    return f'{city} 今天阳光明媚。'

def test_get_weather():

    agent = create_agent(
        model=model,
        tools=[get_weather],
        system_prompt="你是一个智能助手，根据用户的问题进行回答"
    )

    for chunk in agent.stream(
        {
            'messages' : ['青岛今天天气怎么样？'],
        },
        stream_mode=['messages', 'updates'],
        version='v2'
    ):
        # updata类型输出
        if chunk['type'] == 'udpates':

            for node_name, update in chunk['data'].items():

                if node_name == 'model' and update['messages'][-1].tool_calls:

                    print(f'[准备调用工具] : {update['messages'][-1].tool_calls[0]['name']}')

                # 工具执行结果
                elif node_name == 'tools':
                    print(f'【工具返回】:{update['messages'][-1].content}')
        elif chunk['type'] == 'messages':

            token, metadata = chunk['data'] # 元组

            if isinstance(token, AIMessageChunk) and token.content:
                print(f'{token.content}',end= "",flush=True)

@tool
def search_database(query: str) -> str:
    """根据关键词，从数据库中进行查询"""

    writer = get_stream_writer()

    writer(f'正在搜索关键词:{query}')

    time.sleep(1)
    writer(f'找到了50条相关的记录')
    time.sleep(1)

    writer("正在整理最佳答案")

    return f'关于{query}的查询结果'


def test_custom():

    agent = create_agent(
        model=model,
        tools=[search_database],
        system_prompt='你是一个智能助手，根据用户的问题进行回答'
    )

    for chunk in agent.stream(
        {
            'messages' : [HumanMessage("搜索LangChain教程")]
        },
        stream_mode=['messages', 'custom'],
        version='v2'
    ):
        if chunk['type'] == 'custom':
            print(f'【进度】:{chunk['data']}')

        elif chunk['type'] == 'messages':

            token, metadata = chunk['data']

            if isinstance(token, AIMessageChunk) and token.content:
                print(f'{token.content}' , end='', flush=True)


test_custom()
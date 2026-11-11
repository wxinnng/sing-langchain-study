from provide_chat_model import get_chat_model_with_default_setting
from langchain.tools import tool,ToolRuntime
from langchain.agents import create_agent
from langchain.messages import HumanMessage,AIMessage
from dataclasses import dataclass

model = get_chat_model_with_default_setting()

# 定义上下文结构
@dataclass  # 类似于Java里面的@Data注释
class UserContext:

    user_id: str

# 获取用户所在的城市
@tool(description="获取用户所在的城市")
def get_user_city(runtime: ToolRuntime[UserContext]) -> str :
    """获取用户当前所在的城市"""

    # ToolRuntime[UserContext]在这只是指定一下类型
    user_id = runtime.context.user_id # 从上下文环境中获取user_id

    # 模拟用户位置数据库
    user_location = {
        'user_id_1' : "北京",
        'user_id_2' : '上海',
        'user_id_3' : '青岛'
    }

    return user_location.get(user_id,'未知城市')

# 查询指定城市的天气
@tool
def get_city_weather(city: str) -> str:
    """查询指定城市的天气"""

     # 模拟查询天气数据,实际从api获取
    weather_data={
        "北京": "北京小雨，气温10-18℃",
        "上海": "上海暴雨，气温15-22",
        "广州": "广州晴转多云，气温20-28℃",
    }
    return f"{weather_data.get(city, '未知天气')}"


def test_multi_tools():

    agent = create_agent(
        model=model,
        tools=[get_city_weather,get_user_city]
    )

    response = agent.invoke(
        {
            'messages':[
                HumanMessage("今天的天气如何？")
            ]
        },
        context=UserContext(user_id='user_id_2')
    )

    print(response['messages'][-1].content)


test_multi_tools()

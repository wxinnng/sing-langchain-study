from typing import Callable, NotRequired
from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from provide_chat_model import get_chat_model_with_default_setting,get_advanced_model

# 自定义Agent状态
# 在AgentState中就有State了
class CustomStatus(AgentState):

    user_level : NotRequired[int]

simple_model = get_chat_model_with_default_setting()

complex_model = get_advanced_model()


# 动态模型切换中间件
@wrap_model_call
def dynamic_model_selector(
    request: ModelRequest, handler: Callable[[ModelRequest],ModelResponse]
) -> ModelResponse:

    # 获取用户等级
    user_level = request.state.get('user_level', 0)

    # 普通用户使用轻量级
    if user_level == 0:
        target_model = simple_model
    else:
        target_model = complex_model

    return handler(request.override(model=target_model))



agent = create_agent(
    model=simple_model,
    state_schema=CustomStatus,
    middleware=[
        dynamic_model_selector
    ]
)

response = agent.invoke(
    {
        'messages':[
            HumanMessage("你好，你是哪个模型？是gpt-5.6-luna还是gpt-6-luna")
        ],
        'user_level': 1,# VIP用户
    }
)

print(response['messages'][-1].content)

from provide_chat_model import get_chat_model_with_default_setting,get_advanced_model
from typing import NotRequired
from langchain.agents import AgentState,create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import (
    dynamic_prompt,
    ModelRequest,
)


model = get_chat_model_with_default_setting()

# 自定义AgentState
class CustomStatus(AgentState) :

    # 代表这个参数是可选地，在调用的时候可以不传
    user_role : NotRequired[str]


# 动态提示词中间件
@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """根据用户的角色，动态的生成提示词"""

    # 在运行的时候，根据用户的角色，从上下文信息中，获取角色信息，默认为：普通用户
    user_role = request.state.get('user_role','beginner')

    base_prompt = "你是专业的LangChain v1.2 智能体开发应用"


    # 角色差异化
    if user_role == "expert":
        return f"{base_prompt} 输出专业、详尽、带源码解析、带底层原理的技术回答。"
    
    elif user_role == "beginner":
        return f"{base_prompt} 语言通俗易懂，避免专业黑话，步骤清晰，新手友好。"
    
    elif user_role == "admin":
        return f"{base_prompt} 开启调试模式，输出完整日志、报错分析、优化方案。"

    return base_prompt

agent = create_agent(

    state_schema=CustomStatus,
    model=model,
    middleware=[user_role_prompt]
)



from provide_chat_model import get_chat_model_with_default_setting

from langchain.messages import HumanMessage

from langchain.agents import create_agent

model = get_chat_model_with_default_setting()


def test1():
    """
    在设计系统提示词的时候必须：
    1. 角色定义清晰
    2. 强制输出格式
    3. 制定规则
    4. 设定清晰地边界
    5. 提供例子
    """
    agent = create_agent(
     
        model= model,
        system_prompt="你是一位翻译专家,将中文翻译成英文！"
    )

    resposne = agent.invoke({
        'messages':[HumanMessage("中华民族共同体")]
    })

    print(resposne['messages'][-1])



from provide_chat_model import get_chat_model_with_default_setting
from langchain.tools import tool,ToolRuntime
from langchain.agents import create_agent
from langchain.messages import HumanMessage,AIMessage

model = get_chat_model_with_default_setting()


# LangChain v1.2 中，ToolRuntime 是一项核心升级。它会在工具执行时，自动将当前 Agent 的运行环境注入到工具中

@tool
def get_user_question_count(runtime: ToolRuntime) -> str:
    """统计当前会话中用户提出问题的总数量，当用户询问自己问了几个问题时，进行调用"""

    # 从State中获取所有的对话消息
    all_messages = runtime.state['messages']

    username = runtime.state['username'] # wangxing

    # 统计用户发送的信息的数量
    user_message_count = len(
        [msg for msg in all_messages if isinstance(msg , HumanMessage)]
    )

    for msg in all_messages:
        print(msg)


    return f'当前会话中，您一共提出了：{user_message_count}个问题'


def test_get_user_question_count():
    
    agent = create_agent(
        model = model,
        tools=[
            get_user_question_count
        ],
        system_prompt="你是一个智能客服助手，回答用户的提问和帮助用户解决问题",
    )

    # 在这个对象里面设置的属性，都可以在Toolruntime.state里拿到

    response = agent.invoke({
        'messages' : [
            HumanMessage("我想买iPhone 16"),
            AIMessage("好的，iPhone 16 是我们的热门商品。"),
            HumanMessage("现在有货吗？"),
            AIMessage("库存充足，需要我帮你下单吗？"),
            HumanMessage("我问了多少个问题了？"), 
        ],
        'username':'wangxing'
    })

    print(response['messages'][-1].content)


# test_get_user_question_count()

# 获取用户上下文信息
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id : str
    user_level : int = 2

# 获取用户当前的信息
@tool
def get_user_info(runtime : ToolRuntime) :
    """获取当前用户信息，并且根据等级返回不同的权限说明"""

    ctx = runtime.context # 用户当前上下文信息
    user_id = ctx.user_id
    level = ctx.user_level

    if level == 1:
        return (
            f" 用户 {user_id}（VIP会员）特权：无限制访问，可查询历史订单、专属折扣。"
        )
    else:
        return f" 用户 {user_id}（普通用户）限制：仅可查询本月订单，每日限查询 3 次。"

def test_get_user_info():

    agent = create_agent(
        model = model,
        tools=[get_user_info],
        context_schema=UserContext, #指定Context_schema
        system_prompt="你是客服助手，了解用户身份之后，在提供相应的服务！"
    )

    # 调用时注入具体的上下文信息
    response = agent.invoke(
        {
            'messages' : [
                HumanMessage(content="请问我的账户有什么权限？")
            ],
        },
        context=UserContext(user_id="user_id_1001", user_level=1)
    )





    print(response['messages'][-1].content)


test_get_user_info()
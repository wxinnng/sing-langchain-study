from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from provide_chat_model import get_chat_model_with_default_setting


model = get_chat_model_with_default_setting()




def test1():

    #手动构建对话历史
    messages = [
        SystemMessage(content="你是一位翻译专家，将中文翻译成英文。"),
        HumanMessage(content="你好，世界"),
        AIMessage(content="hello, world"),
        HumanMessage(content="我正在写博客"),#当前问题
    ]

    response = model.invoke(
        input=messages
    )

    print(response.content)




def test2():

    messages = [
        {"role": "system", "content": "你是一位翻译专家，将中文翻译成英文。"},
        {"role": "user", "content": "你好，世界"},
        {"role": "assistant", "content": "hell,word"},
        {"role": "user", "content": "我正在写博客"},
    ]

    response = model.invoke(
        input=messages
    )

    print(response.content)

from langchain.agents import create_agent

def test03():

    agent = create_agent(
        model=model
    )

    messages = [
        SystemMessage(content="你是一位翻译专家，将中文翻译成英文。"),
        HumanMessage(content="你好，世界"),
        AIMessage(content="hello, world"),
        HumanMessage(content="我正在写博客"),#当前问题
    ]

    # 对Agent进行传参，一般是传一个字典，然后字典里有一个messages 的 key传入对应的value即可
    response = agent.invoke(
        {
            'messages' : messages
        }
    )

    # 返回结果是中也有一个messages对象，这个对象是一个完整的消息列表
    print(response['messages'][-1].content)

# test03()


def toolMessage():

    tool_call_id = 'call_123'

    # 构造工具的返回消息
    tool_message = ToolMessage(
        content='今天青岛的天气是晴朗，20摄氏度',
        tool_call_id = tool_call_id
    )

    messages = [
        HumanMessage(
            content="今天青岛的天气如何?"
        ),
    ]

    messages.append(tool_message)

    # 交个模型
    response = model.invoke(
       input=messages
    )

    print(response.content)

toolMessage()
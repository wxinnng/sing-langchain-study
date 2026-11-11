from provide_chat_model import get_chat_model_with_default_setting
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.messages import HumanMessage

model = get_chat_model_with_default_setting()


# 初始化内存级记忆引擎
checkpointer = InMemorySaver()
agent = create_agent(
    model=model, 
    checkpointer=checkpointer #绑定记忆引擎，开启记忆能力
    )

#小明的会话id
config_xiaoming = {"configurable": {"thread_id": "1"}}
#小红的会话id
config_xiaohone = {"configurable": {"thread_id": "2"}}

# 小明的对话
print('—————— 以下是小明对话 ——————')
agent.invoke(
    {"messages": [HumanMessage('你好，我叫小明，我的工号是10001')]},
    config=config_xiaoming
)
response1= agent.invoke(
    {"messages": [HumanMessage('我的工号是多少？')]},
    config=config_xiaoming
)
print(f"小明的AI回复：{response1["messages"][-1].content}")

# 小明的对话
print('—————— 以下是小红对话 ——————')
agent.invoke(
    {"messages": [HumanMessage('你好，我叫小红，我的工号是20002')]},
    config=config_xiaohone
)
response2= agent.invoke(
    {"messages": [HumanMessage('我的工号是多少？')]},
    config=config_xiaohone
)
print(f"小红的AI回复：{response2["messages"][-1].content}")

# 验证会话隔离：小红的会话里，无法获取小明的信息
print("—————— 验证会话隔离 ——————")

response3= agent.invoke(
    {"messages": [HumanMessage('你知道小明的工号是多少吗？')]},
    config=config_xiaohone
)

print(f"验证会话隔离回复：{response3["messages"][-1].content}")

from provide_chat_model import get_chat_model_with_default_setting
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

model = get_chat_model_with_default_setting()

# 初始化内存级别存储
# 进程重启之后，就会丢失
# 相同的thread_id共享一份数据，不同的用户必须配置不同的id
checkpoint = InMemorySaver()

agent = create_agent(
    model=model,
    checkpointer=checkpoint # 绑定记忆引擎，开启记忆能力
)

# 配置会话ID
config = {
    'configurable' : {
        'thread_id' : '1001'
    }
}

#第一轮，告诉模型你的名字
response1 = agent.invoke(
    {
        'messages' : {
            'role' : 'human',
            'content':'我叫sing'
        }
    },
    config=config
)

print(response1['messages'][-1].content)


# 第二轮
response2 = agent.invoke(
    {
        'messages':{
            'role':'human',
            'content':'我叫什么名字'
        }
    },
    config=config
)
print(response2['messages'][-1].content)

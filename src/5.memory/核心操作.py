from provide_chat_model import get_chat_model_with_default_setting
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain.agents import create_agent
from langchain.messages import HumanMessage,AIMessage,RemoveMessage

model = get_chat_model_with_default_setting()


# 手动读取记忆
def read_memory():

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        checkpointer=checkpointer
    )

    config = {
        'configurable' : {
            'thread_id' : '1001'
        }
    }

    # 第一论对话
    agent.invoke(
        {
            'messages' : [HumanMessage('你好，我叫小明')]
        },
        config=config
    )

    # 第二轮对话
    response = agent.invoke(
        {
            'messages': [HumanMessage("我叫什么名字")]
        },
        config=config
    )


    checkpointer_tuple = checkpointer.get_tuple(config=config)

    if(checkpointer_tuple):
        # 获取对话历史
        messages = checkpointer_tuple.checkpoint["channel_values"]["messages"]
        print(messages)

# read_memory()

def read_memory_by_agent():

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        checkpointer=checkpointer
    )

    config = {
        'configurable' : {
            'thread_id' : '1001'
        }
    }

    # 第一论对话
    agent.invoke(
        {
            'messages' : [HumanMessage('你好，我叫小明')]
        },
        config=config
    )

    # 第二轮对话
    response = agent.invoke(
        {
            'messages': [HumanMessage("我叫什么名字")]
        },
        config=config
    )


    state = agent.get_state(config=config)

    messages = state.values['messages']

    print(messages, 'messages')

# read_memory_by_agent()

def modify_memory():

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        checkpointer=checkpointer
    )

    config = {
        'configurable':{
            'thread_id' : '1001'
        }

    }

    agent.invoke({
        'messages' : [
            HumanMessage('你好，我叫小明')
        ]
    },
    config=config
    
    )

    agent.invoke(
        {
            'messages':'我叫什么名字'
        },
        config=config
    )
    #这样会被放到最后
    agent.update_state(
        config,{
            'messages' : [AIMessage(content='[系统备注] 这是一条系统消息')]
        }
    )

    state = agent.get_state(config=config)

    id = state.values['messages'][-1].id


    # 删除消息
    agent.update_state(
        config,{
            'messages' : [RemoveMessage(id=id)]
        }
    )

    state = agent.get_state(config=config)
    messages = state.values['messages']
    print(messages, 'messages')

    # 清空所有的信息
    agent.update_state(
        config,
        {
            'messages' : [
                RemoveMessage(id=REMOVE_ALL_MESSAGES), # 清空所有的信息
                HumanMessage(content="新内容") # 这样可以继续添加信息内容
            ]
        }
    )

    # 消息替换
    new_messages = []

    for msg in messages:

        if(msg.content == '你好，我是小明'):
            #替换成新的消息
            new_msg = type(msg)(content = "这是替换后的消息", id=msg.id)
        else:
            new_messages.append(msg)

    # updata方法不是覆盖，而是reducer累加处理
    agent.update_state(
        config,
        {
            'messages' : [
                RemoveMessage(id = REMOVE_ALL_MESSAGES),
                *new_messages
            ]
        }
    )

modify_memory()


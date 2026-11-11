from langgraph.checkpoint.postgres import PostgresSaver
from provide_chat_model import get_chat_model_with_default_setting
from langchain.agents import create_agent
from langchain.messages import HumanMessage

model = get_chat_model_with_default_setting()

DB_URL = 'postgresql://rag:rag@localhost:5433/rag'

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:

    # 首次运行时创建的表
    # checkpointer.setup()

    config = {
        'configurable' : {
            'thread_id' : '1001'
        }
    }

    agent = create_agent(
        model = model,
        system_prompt='你是一个智能助手，请根据用户提问作答',
        checkpointer=checkpointer,
    )

    agent.invoke(
        {
            'messages' : [HumanMessage("你好我叫小明")]
        },
        config=config
    )
    response = agent.invoke({"messages": [HumanMessage("我叫什么名字")]}, config=config)


    print(response['messages'][-1].content)
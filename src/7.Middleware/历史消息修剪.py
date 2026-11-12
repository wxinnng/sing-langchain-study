from typing import Callable
from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage, RemoveMessage
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import (
    after_model,
    before_model,
    wrap_model_call,
    ModelRequest,
    ModelResponse,
)
from langgraph.runtime import Runtime


from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from provide_chat_model import get_chat_model_with_default_setting

model = get_chat_model_with_default_setting()

# 修剪历史消息的中间件
@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, any] | None:
    """保留首条消息和最近的10条消息，移除中间冗余的消息，使对话的长度保持在合理的长度内"""

    messages = state['messages']

    # 如果消息长度小于11，就不需要修剪
    if len(messages) < 11:

        return None

    else :

        first_message = messages[0]
        recent_messages = messages[-10 : ] # 保留最后10条

        new_messages = [first_message] + recent_messages
        
        return {
            'messages' : [
                RemoveMessage(
                    id = REMOVE_ALL_MESSAGES
                ),
                * new_messages
            ],
        }

@wrap_model_call
def check_messages(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:

    messages = request.state.get("messages", )

    print(f'历史消息长度: {len(messages)}', 'dynamic_model_selector')

    return handler(request)

# 短期记忆
checkpointer = InMemorySaver()

agent = create_agent(
    system_prompt="你是一个智能助手，根据用户的提问回答问题",
    model=model,
    middleware=[
        trim_messages, check_messages
    ],
    checkpointer=checkpointer
)

while True:

    answer = input('【提问】：请输入问题')

    res = agent.invoke(
        {
            'messages':[
                HumanMessage(answer)
            ]
        },
        config={
            'configurable' : {
                'thread_id' : '1001'
            }
        }
    )

    print(f'【回答】:{res['messages'][-1].content}',end='\n', flush=True)



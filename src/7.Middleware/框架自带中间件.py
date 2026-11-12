from provide_chat_model import get_chat_model_with_default_setting,get_advanced_model
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware,ToolRetryMiddleware,PIIMiddleware,TodoListMiddleware,HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langgraph.graph.state import Command

model = get_chat_model_with_default_setting()



# 上下文摘要中间件
def test_summarizationMiddleWare():

    # 记忆点
    checkpointer = InMemorySaver()

    agent = create_agent(
        model = model,
        checkpointer=checkpointer,
        middleware=[
            SummarizationMiddleware(
                model = model,

                trigger=[
                    ('tokens',4000),
                    ('messages', 20),
                ],

                keep = ('messages',10)
            )
        ]

    )

@tool
def search(quesiton:str) -> str:
    """进行联网搜搜"""
    return str+"的答案"
@tool
def api_tool(url: str) -> str:
    """进行后端API调用"""
    return url+"响应的内容"

# 工具重试
def test_toolRetryMiddleWare():

    agent = create_agent(
        model = model,
        tools=[api_tool, search],
        middleware=[
            ToolRetryMiddleware(
                max_retries=3,
                backoff_factor=2.0 ,# 等待时间，以2的倍数增长
                initial_delay=1.0,  # 首次等待一秒
                tools=['search'],    # 对哪些工具生效
                retry_on=[ConnectionError,TimeoutError],  # 对那些异常生效
                on_failure='return_message'  # 耗尽重试次数，是将异常返回给用户，而不是抛出异常。
            )
        ]
    )


# 敏感信息脱敏中间件
def test_PIIMidleware():

    agent = create_agent(
        model=model,
        tools=[],
        middleware=[

            # 自动脱敏，邮箱手机号
            PIIMiddleware('email', strategy='redact', apply_to_input=True),
            PIIMiddleware('phone_number', strategy='mask',apply_to_input=True) 
        ]
    )

# 任务规划与跟踪能力中间件
"""
    TodoListMiddleware 是一个为 LangChain Agent 提供待办事项列表（Todo List）管理功能的中间件。它的核心思路是为 Agent 
添加一个专用的write_todos工具，引导 Agent 在接到复杂任务时，先进行规划。
"""
@tool
def read_file(path: str) -> str:
    """读取文件内容"""

    return path + "文件内容"

@tool
def write_file(path: str) -> str:
    """写内容到目标文件""" 

    return "写入成功！"

@tool
def run_tests() -> str:
    """执行测试"""

    return "测试成功！"

def test_todoListMiddleware():

    agent = create_agent(
        model=model,
        tools = [read_file, write_file, run_tests],
        middleware=[
            TodoListMiddleware(
                system_prompt="请根据用户需求创建任务清单,按照优先级执行并更新进度",
                tool_description="write_todos:创建或更新任务清单，格式为：- [ ] 任务描述"
            )
        ]
    )

# 人机审核中间件
@tool
def delete_user(condition: str) -> str:
    """删除用户数据"""
    print("用户信息删除成功！")
    return f'执行删除任务成功，删除数据,条件={condition}'

@tool
def send_msg(email: str, subject: str, content: str) -> str:
    """发送邮件"""
    print("邮件发送成功！")
    return (
        f'【实际结果】\n'
        f'收件人：{email}\n'
        f'主题:{subject}\n'
        f'实际发送内容:{content}\n'
        f'状态:发送成功！'
    )

def test_humanMessage():

    # 内存记忆点
    checkpointer = InMemorySaver()

    agent = create_agent(
        model = model,
        tools=[delete_user, send_msg],
        checkpointer=checkpointer,
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={# 设置审核工具
                    'delete_user' : {
                        'allowed_decisions':[
                            'approve','reject',
                        ]
                    },
                    'send_msg' : {
                        'allowed_decisions':[
                            'approve','reject'
                        ]
                    }    
                }
            )
        ],
    )

    config = {
        'configurable':{
            'thread_id' : '1001'
        }
    }

    result = agent.invoke(
        {
            'messages' : [
                HumanMessage(
                    "删除创建与2025年的用户数据，并发送邮件个132@qq.com.主题：hello ,内容：很高兴认识你！"
                )
            ]
        },
        config=config,
        version='v2'
    )

    is_interrupted = bool(hasattr(result, "interrupts") and result.interrupts)
    if is_interrupted:

        interrupt_value = result.interrupts[0].value
        decisions = []  # 审批意见

        # 原审批数据
        action_requests = interrupt_value["action_requests"]

        # 遍历需要审批的工具
        for i, item in enumerate(interrupt_value["review_configs"]):
            # 模拟用户选择审批意见
            review_input = input(
                f"工具名称：{item['action_name']},请输入审批意见（{','.join(item['allowed_decisions'])})"
            )
            # 发送邮件审核为人工编辑
            if review_input == "edit" and item["action_name"] == "send_msg":
                # 修改邮件内容
                new_msg_content = input("请输入修改后邮件内容：")
                decisions.append(
                    {
                        "type": review_input,
                        "edited_action": {
                            "name": item["action_name"],
                            "args": {
                                **action_requests[i]["args"],  # 保留原来邮件地址和主题
                                "content": new_msg_content,
                            },
                        },
                    }
                )
            else:
                decisions.append({"type": review_input})

        # 提交审批意见
        response = agent.invoke(
            Command(resume={
                        "decisions": decisions
                        }),
            config=config, 
            version="v2"
        )

        print(response.value["messages"][-1].content, "contentvalue")




test_humanMessage()
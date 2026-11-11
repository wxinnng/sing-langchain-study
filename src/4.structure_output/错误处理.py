from provide_chat_model import get_chat_model_with_default_setting
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dataclasses import dataclass
from langchain.agents.structured_output import MultipleStructuredOutputsError, ProviderStrategy, StructuredOutputValidationError
from pydantic import BaseModel,Field, ValidationError
from typing import Optional
from langchain.agents.structured_output import ToolStrategy

model = get_chat_model_with_default_setting()


class Movie(BaseModel):
    """电影参数"""

    year : str = Field(description="电影上映的时间")
    actor: str = Field(description="演员")
    director: str = Field(description="导演")
    rating: Optional[float | None] = Field(
        default=None,
        description="评分",
        ge=1.0,
        le=10.0
    )


# 错误处理
def test_retry():

    # agent = create_agent(
    #     model= model,
    #     response_format=ToolStrategy(
    #         schema=Movie,
    #         handle_errors="评分必须在1-10分之间，请检查"
    #     )
    # )

    agent = create_agent(
        model=model,
        response_format=ToolStrategy(
            schema=Movie,
            handle_errors=ValidationError # 仅仅处理这一种异常
        )
    )

    response = agent.invoke(
        {
            'messages':[
                HumanMessage("""
                    提取电影信息：
                        片名：测试电影
                        年份：2024
                        主演：测试演员
                        导演：测试导演
                        评分：15
                    """)
            ]
        }
    )

    print(response['structured_response'])

# 自定义错误处理函数
def custom_error_handler(error: Exception) -> str:
    """自定义错误处理逻辑"""
    if isinstance(error, StructuredOutputValidationError):
        return "数据格式验证失败：评分必须在 1-10 之间，请修正后重试。"
    elif isinstance(error, MultipleStructuredOutputsError):
        return "错误：返回了多个结果，请只选择最相关的一个。"
    else:
        return f"未知错误：{str(error)}"


def define_function():
    
    # 创建agent - 使用自定义错误处理函数
    agent = create_agent(
        model=model,
        response_format=ToolStrategy(
            schema=Movie,
            handle_errors=custom_error_handler,  # 传入自定义函数
        ),
    )

    

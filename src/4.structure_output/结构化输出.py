from provide_chat_model import get_chat_model_with_default_setting
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from dataclasses import dataclass
from langchain.agents.structured_output import ProviderStrategy

model = get_chat_model_with_default_setting()

@dataclass
class User:
    id : str
    name : str


def use_structured_response():

    # 自动判别类型
    agent = create_agent(
        model=model,
        response_format=User,   # 输出格式shame，需要提前设置
    )

    # 适配主流的大模型，

    # agent = create_agent(
    #     model=model,
    #     response_format=ProviderStrategy(
    #         schema=User,
    #         strict=True # 开启严格模式
    #     )
    # )

    # ToolStrategy模式，兼容性最好
    # agent = create_agent(
    #     model=llm,# 模型
    #     response_format=ToolStrategy(
    #         schema=YourSchema, 
    #         handle_errors=True  # 自动重试（默认开启）
    #     )
    # )



    result = agent.invoke(
        {
            'messages' : [
                HumanMessage("给我一首你最喜欢的古诗")
            ]
        }
    )

    structure_data = result['structured_response']

    print(structure_data)

# use_structured_response()


from pydantic import BaseModel, Field
from typing import Optional
from langchain.agents import create_agent

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



# 使用Pydantic的方式
def user_pydantic():

    # 创建Agent
    agent = create_agent(
        model=model,
        system_prompt="你是一个智能助手，请根据用户的提问，来回答问题",
        response_format=Movie
    )

    # 调用模型
    response = agent.invoke({
        'messages' : [
            HumanMessage('泰坦尼克号')
        ]
    })

    structured_response = response['structured_response']

    print(structured_response)#输出year='1997' actor='莱昂纳多·迪卡普里奥' director='詹姆斯·卡梅隆' rating=9
    print(structured_response.year) #上映年份 输出：1997
    print(structured_response.actor) #演员 输出：莱昂纳多·迪卡普里奥
    print(structured_response.director) #导演 输出：詹姆斯·卡梅隆
    print(structured_response.rating) #评分 输出：9

# user_pydantic()

# 通过dataclasses轻量级来实现
@dataclass
class SimpleContact():

    name : str
    phone : str
    email: Optional[str] = None


def test_dataclasses_output():

    agent = create_agent(
        model=model,
        system_prompt="你是一个智能助手，请根据用户的问题进行回答！",
        response_format=SimpleContact
    )

    response = agent.invoke(
        {
            'messages' : [HumanMessage("张三，手机号：1902902922，邮箱：29029032@qq.com")]
        }
    )

    structured_response = response['structured_response']

    print(structured_response.name)
    print(structured_response.phone)
    print(structured_response.email)


# test_dataclasses_output()

from typing import TypedDict


class SimpleContact(TypedDict):

    name: str
    phone: str
    email: str

def test_dict_format():

    agent = create_agent(
        model=model,
        system_prompt="你是一个智能助手，根据用户的问题进行回答",
        response_format=SimpleContact
    )

    # 模型调用
    response = agent.invoke(
        {
            'messages': [HumanMessage("张三，手机号：1902902922，邮箱：29029032@qq.com")]
        },
        
    )['structured_response']

    print(response)


# test_dict_format()


# JSON的格式
# 标准JSON Schema定义
simple_contact_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "用户姓名"},
        "phone": {"type": "string", "description": "用户手机号码"},
        "email": {"type": "string", "description": "用户邮箱地址"}
    },
    "required": ["name",  "phone"],
    "additionalProperties": False
} 

def json_format():

    agent = create_agent(
        model=model,
        system_prompt="你是一个智能助手，给用户回答问题",
        response_format=simple_contact_schema
    )


    response = agent.invoke(
        {
            'messages' : [
                HumanMessage("张三，手机号：1902902922，邮箱：29029032@qq.com")
            ]
        }
    )

    print(response['structured_response'])


json_format()
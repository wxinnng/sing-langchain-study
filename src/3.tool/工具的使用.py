from provide_chat_model import get_chat_model_with_default_setting
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage

model = get_chat_model_with_default_setting()


# 定义工具，从数据库查询数据,一定要给上解释
@tool
def check_stock(product_id: str) -> str:
    """查询商品的库存状态"""
    stock_data = {
        'A101' : 15,
        'B202' : 0,
        'C303' : 1,
    }

    stock = stock_data.get(product_id, 0)

    if stock > 0:
        return f"商品 {product_id} 库存充足，剩余 {stock} 件"
    else:
        return f"商品 {product_id} 已售罄，暂时无货"



def do_check_stock():

    agent = create_agent(
        model= model,
        # 注册工具
        tools=[
            check_stock
        ]
    )

    response = agent.invoke(
        {
            'messages' : [{
                'role': 'human',
                'content' : '帮我查一查编号为B202的物品是否还有库存'
            }]
        }
    )

    print(response['messages'][-1].content)



# do_check_stock()
# 对函数的注释是必须的
@tool
def search_customer_info(customer_name: str, max_result: int = 6) -> str:
    """查询客户信息，当用户需要查找指定客户的资料时调用此工具。
    Args:
        customer_name: 要查询的客户姓名，必填项
        max_result: 返回的最大结果条数，默认为6条
    """
    return f"找到{max_result}条名为【{customer_name}】的客户信息"

# 复杂参数，使用Pydantic来做模型的强校验
from pydantic import BaseModel, Field
from typing import Optional

# 定义参数类型
class EmailInput(BaseModel):
    """邮件发送参数"""

    to:str = Field(description="收件人邮箱地址")
    subject:str = Field(description="邮箱主题")
    body: str = Field(description="邮箱正文内容" , default="")


# 定义工具
@tool
def send_email(param: EmailInput) -> str:
    """
    发送邮件到指定收件人。
    当用户需要发送邮件、通知或报告时使用此工具。
    """

    print("工具已被调用！")

    #模拟发送成功响应
    return f"邮件已发送至 {param.to}，主题：{param.subject},正文内容：{param.body}"

def test_send_email():

    # 模拟邮箱发送
    # model.bind_tools([send_email]) model也可以直接绑定tools，但是不会自己调用
    agent = create_agent(
        model=model,
        tools=[send_email]
    )

    messages = [
        HumanMessage(content="帮我给1320444219@qq.com邮箱发送一份主题为：LangChain学习报告的邮件，正文为：tool的定义与使用")
    ]

    response = agent.invoke(
        {
            'messages' : messages,
        }
    )

    print(response['messages'][-1].content)


# test_send_email()

# 自定义工具名字
@tool('web_search')
def search(query: str) -> str:
    """搜索网页内容"""
    return f'搜索结果{query}+test'

# 覆盖描述
# 方式1：依赖 docstring（默认）
@tool
def calculator(expression: str) -> str:
    """执行数学计算"""  # 模型看到的就是这行
    return str(eval(expression))

# 方式2：显式覆盖（优先级最高）
@tool(description="专门用于处理加减乘除和复杂数学表达式。当用户询问任何数学问题时必须调用此工具。")
def calculator(expression: str) -> str:
    """执行数学计算"""  # 这行会被忽略！
    return str(eval(expression))





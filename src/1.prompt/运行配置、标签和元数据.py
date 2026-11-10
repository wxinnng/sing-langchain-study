from langchain_core.runnables import RunnableConfig,RunnableLambda
from provide_chat_model import get_chat_model_with_default_setting
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


model = get_chat_model_with_default_setting()

# 上一节的，使用一条执行链
summary_chain = (
    ChatPromptTemplate.from_template('用一句话总结{text}')
    | model
    | StrOutputParser()
)

# 这些是给本次的运行打上标签，后期可以使用langsmith进行追踪
config = RunnableConfig(
    tags=['learning', 'summary'],
    metadata={'tenant_id' : 'demo', 'feature' : 'summary'},
    run_name='summary-request'
)

# RunawaybelLambda可以将一个普通的函数，改造成可以与 | 一起使用。
# 里面只是一个lambda函数的写法
"""
def normalize_text(payload):
    return {
        "text": payload["text"].strip()
    }
""" 
normalize = RunnableLambda(
   
    lambda payload: {"text": payload["text"].strip()}
)

chain = normalize | summary_chain


answer = chain.invoke({'text' : 'hello'} , config=config)

print(answer)
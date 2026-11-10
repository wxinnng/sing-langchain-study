from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from provide_chat_model import get_chat_model_with_default_setting
from langchain_core.output_parsers import StrOutputParser

model = get_chat_model_with_default_setting()

def branch_and_parallel():

    summary_chain = (
        ChatPromptTemplate.from_template('用一句话总结{text}')
        | model
        | StrOutputParser()
    )

    keywords_chain = (
        ChatPromptTemplate.from_template('提取三个关键字，只使用逗号分隔开{text}')
        | model
        | StrOutputParser()
    )

    # 这里的参数可以自己设置，同时下面获取的时候，也输入相应的值即可。
    parallel = RunnableParallel(
        wx_summarya = summary_chain,
        keywords = keywords_chain
    )

    results = parallel.invoke({
        'text' : 'LangChain可以把模型，工具和检索组合起来！'
    })

    print(results['wx_summarya'])
    print(results['keywords'])

branch_and_parallel()
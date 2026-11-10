from provide_chat_model import get_chat_model_with_default_setting

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

from langchain_core.messages import HumanMessage,AIMessage

from langchain_core.output_parsers import StrOutputParser

model = get_chat_model_with_default_setting()

def use_string_template():
    prompt = ChatPromptTemplate.from_messages([
    ('system' , '你是一名{role}.回答必须使用中文，而且回答的长度限制在{max_words}以内'),
    ('human' , '请解释 {topic}')
    ])

    messages = prompt.invoke({
        'role' : 'Py教师',
        'max_words' : 100,
        'topic' : 'llama_index'
    })


    response = model.invoke(messages)

    print(response.content)
    print(type(response))


def use_MessagesPlaceholder():

    prompt = ChatPromptTemplate.from_messages([
        ('system' , '你是一个能记住上下文的助手'),
        MessagesPlaceholder('history'),
        ('human', '{question}'),
    ])
    # LCEL（LangChain Expression Language，LangChain 表达式语言）。其实上面写法的语法糖，简单写法
    chain = prompt | model

    response = chain.invoke({
        'history' : [
            HumanMessage(content="我叫小王"),
            AIMessage(content="你好，小王！"),
        ],
        'question' : '我叫什么？',
    })

    print(response.content)


#use_MessagesPlaceholder()


def piple():

    prompt = ChatPromptTemplate.from_messages([
        ('system' , '你是一名{role}.回答必须使用中文，而且回答的长度限制在{max_words}以内'),
        ('human' , '请解释 {topic}')
        ])

    # 调用链 
    chain = prompt | model | StrOutputParser()

    # {} -> prompt -> model -> stroutputparser ,按照这个链条进行执行
    result = chain.invoke({
        'role':"py教师",
        'max_words' : 100,
        'topic' : 'LCEL介绍'
    })

    print(result)


piple()
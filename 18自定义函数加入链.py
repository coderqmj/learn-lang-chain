# 导入chat通议模型
from langchain_community.chat_models.tongyi import ChatTongyi


# 导入模板
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# from 通用提示词模板 import chain


first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}, 刚生了{gender}， 请起名字。请直接返回名字的字符串"
)


# 自定义函数，输入名字字符串，输出json格式
# 普通函数：接收纯字符串 name，直接返回 {"name": name}
def format_name(name: str) -> dict:
    return {"name": name}


# RunnableLambda 包装：接收的是 langchain 的 AIMessage 对象，取其中的 .content 字段再封装
my_fun = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})


second_prompt = PromptTemplate.from_template("帮我解析下名字{name}的含义")


model = ChatTongyi(model="qwen-max", streaming=True)


chain = first_prompt | model | my_fun | second_prompt | model
#


chain.stream(
    {"lastname": "邱", "gender": "男"},
)

for chunk in chain.stream({"lastname": "邱", "gender": "男"}):
    print(chunk.content, end="", flush=True)

from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate

"""
PromptTemplate / FewShotPromptTemplate / ChatPromptTemplate 都属于“提示词模板”这一类。

它们常见的两种用法：
1) format(...)：更偏向“字符串层”的拼接，返回 str（已经把变量填进去的最终提示词文本）
2) invoke({...})：更偏向“Runnable/链式调用层”的执行方式，返回的是模板对象对应的“输出类型”
   - PromptTemplate.invoke(...) 返回 StringPromptValue（可以理解为“封装后的提示词值”）
   - ChatPromptTemplate.invoke(...) 返回 ChatPromptValue（封装后的“消息列表”）

为什么要有 invoke？
因为在 LangChain 的 LCEL（| 管道）里，链的每一段都希望能统一用 invoke/stream/batch 这套接口来“运行”，
模板也不例外：模板本身就是 Runnable 的一环。
"""

template = PromptTemplate.from_template("我的邻居是：{lastname}，最喜欢：{hobby}")

# 1) format：直接得到字符串
res = template.format(lastname="张大明", hobby="钓鱼")
print(res, type(res))

# 2) invoke：得到“PromptValue”（不是 plain string）
res2 = template.invoke({"lastname": "周杰轮", "hobby": "唱歌"})
print(res2, type(res2))

# res vs res2 的区别（重点）：
# - res 是 str：适合你立刻 print / 保存到文件 / 传给你自己的 HTTP 请求等“纯文本”场景
# - res2 是 PromptValue：适合继续接入 LCEL（例如 template | model），并且可以按需转成字符串
print(res2.to_string(), type(res2.to_string()))

# 额外：ChatPromptTemplate 的 invoke 返回 ChatPromptValue（内部是 messages），而不是字符串
chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个严谨的助手"),
        ("human", "把 {word} 用一句话解释清楚"),
    ]
)
chat_value = chat_template.invoke({"word": "向量数据库"})
print(chat_value, type(chat_value))


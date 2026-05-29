# 如果想要封装历史记录，除了自己维护，也可借助LC内置历史记录功能
# 基于RunnableWithMessageHistory在原有链的基础上创建带有历史记录功能的新链（新Runnable实例）
# 基于InMemoryChatMessageHistory为历史记录提供内存存储（临时用）

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory


def print_prompt(full_prompt):
    print("=" * 20, full_prompt.to_string(), "=" * 20)
    return full_prompt


model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template(
    "你需要根据对话历史回应用户问题。对话历史：{chat_history}。用户当前输入：{input}，请给出回应"
)

base_chain = prompt | print_prompt | model | StrOutputParser()


chat_history_store = {}  # 存放多个会话ID所对应的历史会话记录


def get_history(session_id):
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]


# 创建带历史记忆的对话链
# 第一个参数 base_chain：原始对话链（不带记忆），RunnableWithMessageHistory 会在其外层“包装”一层历史记忆能力。
# 第二个参数 get_history：历史记录获取函数；接收 session_id，返回该会话对应的 ChatMessageHistory 实例；
# RunnableWithMessageHistory 会在每次调用时通过它拿到当前会话的历史消息，并在调用后把新消息写回去，实现“记忆”。
# input_messages_key="input"：指定输入字典里“用户当前输入”对应的 key（这里是 {"input": "..."}）。
# history_messages_key="chat_history"：指定历史消息注入到提示词/链路时使用的 key（这里的 PromptTemplate 使用了 {chat_history} 占位符）。
conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# 主程序入口：演示带历史记忆的对话链，连续提问并自动拼接上下文
if __name__ == "__main__":
    # 固定格式，就是这么写的
    session_config = {"configurable": {"session_id": "user_001"}}
    print(conversation_chain.invoke({"input": "小明有一只猫"}, session_config))
    print(conversation_chain.invoke({"input": "小刚有两只狗"}, session_config))
    print(conversation_chain.invoke({"input": "共有几只宠物？"}, session_config))

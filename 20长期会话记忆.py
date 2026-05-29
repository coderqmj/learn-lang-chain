# 实现思路总结（FileChatMessageHistory）：
# 1) 基于文件持久化会话记录：把历史消息写到磁盘文件里，程序退出也不会丢。
# 2) 用 session_id 做隔离：通常以 session_id 作为文件名/文件路径的一部分，不同 session_id 对应不同文件。
# 3) 作为 ChatMessageHistory 的一种实现：继承 BaseChatMessageHistory，主要实现 3 个同步接口：
#    - add_messages：追加写入消息
#    - messages：读取并返回全部消息
#    - clear：清空消息（删除/重置文件内容）
#
# 19 介绍的 memory 是短期记忆：只在内存中保存，程序一旦退出就会丢失。
# 这里介绍长期会话记忆：在多个会话/多次运行之间保持记忆，例如用户在不同时间点的对话记录。
import os, json
from typing import Sequence
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import (
    BaseMessage,
    # 单个消息对象（BaseMessage 的子类）转换成字典
    message_to_dict,
    # message_from_dict,
    # 多个消息对象（BaseMessage 的子类）转换成字典
    messages_to_dict,
    # [字典, 字典, ...] => [消息对象, 消息对象, ...]
    messages_from_dict,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path: str):
        self.session_id = session_id  # 会话 ID，用于隔离不同会话的文件
        self.storage_path = storage_path  # 存储路径，文件名或目录名

        # 类似于JS里面的path.join，用于拼接路径 ，完整的文件路径，包含文件名
        self.file_path = os.path.join(self.storage_path, self.session_id)
        # 确保文件夹存在，不存在则创建，exist_ok=True 表示如果目录已存在，不抛出异常
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # self.messages = []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        # 相当于 [].push
        all_messages.extend(messages)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(messages_to_dict(all_messages), f, ensure_ascii=False, indent=2)

    # 装饰器 @property 表示将方法转换为属性，直接调用即可，不需要加()
    @property
    def messages(self) -> list[BaseMessage]:
        # 处理异常：如果文件不存在，返回空列表
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return messages_from_dict(data)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


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
    return FileChatMessageHistory(session_id, "./chat_history")


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
    # print(conversation_chain.invoke({"input": "小明有一只猫"}, session_config))
    # print(conversation_chain.invoke({"input": "小刚有两只狗"}, session_config))
    print(conversation_chain.invoke({"input": "共有几只宠物？"}, session_config))

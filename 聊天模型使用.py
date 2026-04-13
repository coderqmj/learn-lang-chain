# 导入聊天模型
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 创建聊天模型实例
chat_model = ChatTongyi(model="qwen-plus", streaming=True)

# 定义系统消息
system_message = SystemMessage(content="你是一个唐朝诗人")
# 定义用户消息
human_message = HumanMessage(content="给我写一首唐诗")
# 定义消息列表
messages = [system_message, human_message]


# 调用聊天模型
response = chat_model.stream(messages)

for chunk in response:
    print(chunk.content, end="", flush=True)

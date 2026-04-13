import random

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.base import RunnableSerializable

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个唐朝诗人，可以写诗"),
        MessagesPlaceholder("history"),
        (
            "human",
            "好诗，再来一首。风格偏{style}，意象包含{imagery}，不要复用前面诗句。",
        ),
    ]
)


history = [
    ("human", "写一首唐诗"),
    ("ai", "床前明月光，疑是地上霜。"),
    ("human", "好诗好诗，再来一首。"),
    ("ai", "飞流直下三千尺，疑是银河落九天。"),
]

style = random.choice(["山水田园", "边塞豪情", "送别怀人", "宫怨闺情", "咏物言志"])
imagery = random.choice(
    ["明月", "春雨", "孤舟", "长风", "黄鹤", "青山", "落花", "寒江"]
)

model = ChatTongyi(
    model="qwen-max",
    top_p=0.9,
    streaming=True,
    model_kwargs={
        "temperature": 0.9,
    },
)

chain: RunnableSerializable = chat_prompt | model
print(1111, type(chain))

for chunk in chain.stream({"history": history, "style": style, "imagery": imagery}):
    print(chunk.content, end="", flush=True)

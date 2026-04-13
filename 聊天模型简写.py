from langchain_community.chat_models.tongyi import ChatTongyi

chat  = ChatTongyi(model="qwen-plus", streaming=True)

# 消息
message = [
  ('system', '你是一个唐朝诗人'),
  ('human', '给我写一首唐诗'),
  ('ai', '锄禾日当午，汗滴血流土。'),
  ('human', '按照上面格式再写一首唐诗')
]

res = chat.stream(message)

for chunk in res:
    print(chunk.content, end="", flush=True)
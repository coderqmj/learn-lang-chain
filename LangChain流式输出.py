# LangChain流式输出
from langchain_community.llms.tongyi import Tongyi 

llm = Tongyi(model="qwen-plus", streaming=True)
for chunk in llm.stream("你好，你能做一些什么？"):
    # 将每个流式输出的块(chunk)立即打印到终端，不换行，强制刷新缓冲区
    print(chunk, end="", flush=True)

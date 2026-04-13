# Langchain访问通义千文大模型
from langchain_community.llms.tongyi import Tongyi 

llm = Tongyi(model="qwen-plus")  
print(llm.invoke("你好"))

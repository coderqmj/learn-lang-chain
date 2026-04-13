# 文本嵌入模型
from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings()

# embed_query 用于将输入文本转换为向量表示（嵌入），方便后续语义搜索或相似度计算
print(embeddings.embed_query("你好"))
# embed_documents 用于将多个文档转换为向量表示（嵌入），方便批量处理
print(embeddings.embed_documents(["你好，你能做一些什么？","我喜欢吃鱼", "我爱打游戏"]))



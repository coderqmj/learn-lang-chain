# 想要以第一次模型输出的结果，第一次去询问模型
# 这么操作：创建这个Chain是没有问题的，但是执行是会报错的
# ValueError: Invalid input type <class 'langchain_core.messages.ai.AIMessage'>. Must be a PromptValue, str, or list of BaseMessages.
# 这里说它的输入类型不对，是一个AIMessage，而不是一个字符串或一个PromptValue
# 解决方案：
# 1. StrOutputParser字符串输出解析器，而不是AIMessage
# 2. 将AIMessage转换为字符串

# 导入 模板 和通义模型
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser


# 定义模板
template = PromptTemplate.from_template("你好，{name}")

model = ChatTongyi(model="qwen-plus", streaming=True)
parser = StrOutputParser()

# chain = template | model | model 这里就会报上面的错误
chain = template | model | parser | model


res = chain.invoke(input={"name": "张三"})
print(res.content)

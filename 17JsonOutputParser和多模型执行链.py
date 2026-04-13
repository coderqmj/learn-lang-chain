# 16使用的字符串解析器，将模型结果解析再给模型，这种方案并不标准
# 上一个模型的输出，没有被处理，就输入下一个模型
# 正常情况： invoke|stream 初始输入 => 提示词模板 =>  模型 => 数据处理 => 提示词模板 => 模型 => 解析器 => 结果
# 翻译一下就是，上一个模型输出结果，作为提示词模板的输入，构建下一个提示词，用来二次调用模型，这样才符合大多数场景
# 所以需要 JsonOutputParser 来解析模型结果，将模型结果转换为 JSON 格式


# 导入 模板 和通义模型
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import JsonOutputParser


# 定义模板
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}, 刚生了{gender}， 请起名字，并且封装到JSON格式给我，要求key是name，value就是名字。请严格遵守JSON格式"
)
second_prompt = PromptTemplate.from_template("姓名{name},帮我解析含义")


model = ChatTongyi(model="qwen-plus", streaming=True)
json_parser = JsonOutputParser()

# chain = template | model | model 这里就会报上面的错误
chain = first_prompt | model | json_parser | second_prompt | model
# 上一个模型的输出，作为提示词模板的输入，构建下一个提示词，用来二次调用模型，这样才符合大多数场景


res = chain.stream(input={"lastname": "王", "gender": "女儿"})
for chunk in res:
    print(chunk.content, end="", flush=True)

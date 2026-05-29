# Document Loader 文档加载器

文档加载器提供了一套标准接口，用于将不同来源（如 CSV、PDF 或 JSON 等）的数据读取为 LangChain 的文档格式。这确保了无论数据来源如何，都能对其进行一致性处理。

文档加载器（内置或自行实现）需实现 `BaseLoader` 接口。

---

## Class Document

`Document` 是 LangChain 内文档的统一载体，所有文档加载器最终返回此类的实例。

### 创建示例

```python
from langchain_core.documents import Document

document = Document(
    page_content="Hello, world!", 
    metadata={"source": "https://example.com"}
)


# Document Loaders 文档加载器

## 统一接口

不同的文档加载器可能定义了不同的参数，但是它们都实现了统一的接口方法：

| 方法 | 说明 |
|------|------|
| `load()` | 一次性加载全部文档 |
| `lazy_load()` | 延迟流式传输文档，对大型数据集很有用，避免内存溢出 |

---

## 使用示例：CSVLoader

```python
from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    ... # 初始化参数
)

# 一次性加载全部文档
documents = loader.load()

# 对于大数据集，分段返回文档
for document in loader.lazy_load():
    print(document)
```

# CSVLoader

自定义 CSV 文件的解析和加载。

## 使用示例

```python
loader = CSVLoader(
    file_path="../../xxx.csv",
    csv_args={
        "delimiter": ",",        # 指定分隔符
        "quotechar": "'",        # 指定字符串的引号包裹
        "fieldnames": ["name", "age", "gender"],  # 字段列表
        # 注意：无表头时使用 fieldnames
        # 有表头时请勿使用，否则会将首行当作数据读取
    }
)

data = loader.load()
print(data)
```
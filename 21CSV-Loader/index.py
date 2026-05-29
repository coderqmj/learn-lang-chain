from pathlib import Path

from langchain_community.document_loaders import CSVLoader


csv_path = Path(__file__).resolve().parent / "stu.csv"
loader = CSVLoader(
    file_path=str(csv_path),
    encoding="utf-8",
)

# 批量加载文档
# documents = loader.load()
# print(documents)

# 懒加载
documents = loader.lazy_load()

for document in documents:
    print(1111, document)
    print("-----------------")

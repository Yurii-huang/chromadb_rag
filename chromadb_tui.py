import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 初始化 ChromaDB 客户端和集合
try:
    client = chromadb.PersistentClient(path='vectorstore/db_chroma', settings=Settings(anonymized_telemetry=False))
    collection = client.get_collection(name="pdf_collection")
except chromadb.errors.InvalidCollectionException:
    collection = client.create_collection(name="pdf_collection")
    logging.info("集合 'pdf_collection' 不存在，已创建新集合。")
except Exception as e:
    logging.error(f"连接到 ChromaDB 数据库时出错: {e}")
    collection = None

# 初始化 HuggingFaceEmbeddings
try:
    # 指定本地缓存目录
    cache_dir = 'HuggingFaceEmbeddings'
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L12-v2',
        model_kwargs={'device': 'cpu'},
        cache_folder=cache_dir
    )
except Exception as e:
    logging.error(f"初始化嵌入模型时出错: {e}")
    embeddings = None


def query_chromadb(query):
    if collection is None:
        return "无法连接到 ChromaDB 集合，请检查配置。"
    elif embeddings is None:
        return "嵌入模型初始化失败，请检查配置。"
    try:
        query_embedding = embeddings.embed_query(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        return results['documents'][0][0] if results['documents'][0] else "未找到相关结果。"
    except Exception as e:
        return f"查询过程中出现错误: {e}"


if __name__ == "__main__":
    print("欢迎使用 ChromaDB 查询工具，输入 'q' 退出。")
    while True:
        user_input = input("请输入查询内容: ")
        if user_input.lower() == 'q':
            break
        elif user_input == "#clear":
            import os
            if os.name == 'nt':  # 针对 Windows 系统
                os.system('cls')
            else:  # 针对 Linux/Mac 系统
                os.system('clear')
            print("历史消息已清除。")
            continue
        elif user_input.startswith('#'):
            print(f"当前执行工具命令: {user_input}，但此命令无具体执行逻辑。")
            continue
        result = query_chromadb(user_input)
        print(f"🤖 为您检索到以下信息：\n{result}")
from flask import Flask, request, render_template, jsonify
import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 修改 static_folder 和 template_folder 为 static
app = Flask(__name__, template_folder='static', static_folder='static')

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


def query_chroma(question):
    if collection is None:
        return "无法连接到 ChromaDB 集合，请检查配置。"
    if embeddings is None:
        return "嵌入模型初始化失败，请检查配置。"
    try:
        query_embedding = embeddings.embed_query(question)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        documents = results.get('documents', [[]])[0]
        if documents:
            result = "\n".join(map(str, documents))
        else:
            result = "未找到相关结果，请尝试其他问题。"
        return result
    except Exception as e:
        return f"查询过程中出现错误: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form.get('question')
        if question:
            logging.info(f"收到查询问题: {question}")
            try:
                result = query_chroma(question)
                logging.info(f"查询结果: {result}")
                return jsonify({"result": result})
            except Exception as e:
                # 查询失败，返回错误信息
                error_message = f"查询出错: {str(e)}"
                logging.error(error_message)
                return jsonify({"error": error_message}), 500
    return render_template('index.html')


if __name__ == "__main__":

    app.run(host='localhost', port=5000, debug=True)
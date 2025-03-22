# Import necessary modules
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
import os
import threading
import logging

# Define paths
data_dir = 'data/'
chroma_db = 'vectorstore/db_chroma'

# Function to create a vector database
def create_vector_db():
    # Check if the directory exists, if not, create it
    if not os.path.exists(data_dir):
        os.makedirs(chroma_db )
    
    # Create a DirectoryLoader instance to load PDF documents
    loader = DirectoryLoader(data_dir,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader,
                             use_multithreading=True)
    
    # Load documents from the directory
    document = loader.load()
    print('.....document_loaded.....')
    
    # Initialize a text splitter to divide documents into chunks
    # 初始化一个文本分割器，用于将文档分割成小块
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    print('.....document_splitter.....')
    
    # Split documents into smaller text chunks
    # 将文档分割成更小的文本块
    texts = text_splitter.split_documents(document)
    print('.....document_splitted.....')
    
    # Initialize HuggingFaceEmbeddings using a specific model
    # 使用特定模型初始化 HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L12-v2',
                                       model_kwargs={'device': 'cpu'})
    print('.....document_embedded.....')
    
    # Create a vector store using Chroma from the text chunks and embeddings
    # 尝试使用文本块和嵌入向量通过 Chroma 创建向量存储
    try:
        # 明确指定集合名称为 pdf_collection
        db = Chroma.from_documents(texts, embeddings, persist_directory=chroma_db, collection_name="pdf_collection")
        logging.info('向量数据库已成功创建并持久化到 %s', chroma_db)
    except Exception as e:
        # 若创建向量数据库失败，记录错误日志并抛出异常
        logging.error('创建向量数据库失败: %s', e)
        raise
    print('.....document_loaded_at_db.....')
    
    # # Save the vector store locally
    # # 注释掉的代码，因为 Chroma 已在创建时持久化，无需此操作
    # db.save_local(chroma_db)

if __name__ == "__main__":
    # Create a new thread to execute the function
    # 创建一个新线程来执行创建向量数据库的函数
    document_thread = threading.Thread(target=create_vector_db)
    document_thread.start()
    document_thread.join()

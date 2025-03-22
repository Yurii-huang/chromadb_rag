# ChromaDB 项目使用指南

## 一、项目概述
本项目借助 ChromaDB 搭建了一个支持向量存储与查询的系统。该系统提供了两种查询途径，分别是 Web 界面和终端交互界面（TUI），并且支持把 PDF 数据导入向量数据库。

## 二、项目结构
```plaintext
.venv/                       # 虚拟环境目录
.vscode/                     # VSCode 配置目录
HuggingFaceEmbeddings/       # Hugging Face 嵌入模型缓存目录
  .locks/
  models--sentence-transformers--all-MiniLM-L12-v2/
chromadb_loader.py           # 用于将 PDF 数据导入向量数据库
chromadb_tui.py              # 终端交互界面脚本
chromadb_web_query.py        # Web 界面服务脚本
data/                        # 存放待导入的 PDF 文件
static/                      # Web 界面静态资源目录
  index.html
vectorstore/                 # 向量数据库存储目录
  db_chroma/
```

三、环境准备
1. 创建虚拟环境
    ```bash
    python -m venv .venv
    ```

2. 激活虚拟环境
    `Linux/Mac`：

    ```bash
    source .venv/bin/activate
    ```

    Windows：
    ```bash
    .venv\Scripts\activate
    ```
3. 安装依赖

    ```bash
    pip install -r requirements.txt
    ```

四、导入 `PDF` 数据

1. 准备 `PDF` 文件，将需要导入的 `PDF` 文件放置在 `data/` 目录下。

2. 运行导入脚本

    ```bash
    python chromadb_loader.py
    ```

    脚本会执行以下操作：

    - 读取 `data/` 目录下的所有 `PDF` 文件。
    - 使用 `langchain` 对 `PDF` 内容进行分割和处理。
    - 利用 `HuggingFaceEmbeddings` 生成向量嵌入。
    - 将处理后的数据存储到 `ChromaDB` 的 `pdf_collection` 集合中。

五、使用 `Web` 界面进行查询
1. 启动 `Web` 服务

    ```bash
    python chromadb_web_query.py
    ```

2. 访问 `Web` 界面
    打开浏览器，访问 `http://localhost:5000`。

3. 输入查询内容
在输入框中输入查询问题，点击提交按钮，系统将返回查询结果。

六、使用终端交互界面（`TUI`）进行查询
1. 启动 `TUI` 程序

    ```bash
    python chromadb_tui.py
    ```

2. 输入查询内容，按照提示输入查询问题，按回车键提交查询，系统将返回查询结果。

3. 特殊命令

- 退出程序：输入 `q` 并按回车键退出。
- 清除历史消息：输入 `#clean` 并按回车键清除终端历史消息。
- 工具命令：输入以 `#` 开头的其他命令，系统将提示该命令无具体执行逻辑。

七、注意事项

- 确保 `data/` 目录下有有效的 `PDF` 文件，否则导入过程将无数据可处理。
- 若遇到 `ChromaDB` 连接问题或嵌入模型初始化失败，请检查配置和日志信息。
- 使用 `Web` 界面时，确保 `Flask` 服务正常运行，若端口被占用，可修改 `chromadb_web_query.py` 中的端口配置。
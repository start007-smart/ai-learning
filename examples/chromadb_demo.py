import chromadb

# 本地测试的话，先安装 pip3 install chromadb

def main():
    # 1. 初始化 Chroma 客户端 
    # 这里使用的是内存模式，程序结束数据也就消失了。
    # 如果你想把数据保存在本地硬盘，可以使用: 
    # client = chromadb.PersistentClient(path="./my_chroma_data")
    print("正在初始化 ChromaDB 客户端...")
    client = chromadb.Client()

    # 2. 创建或获取一个集合 (Collection)，相当于关系型数据库中的表
    collection_name = "demo_collection"
    # 为了演示，如果存在就先删除
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
        
    collection = client.create_collection(name=collection_name)
    print(f"成功创建集合: {collection_name}")

    # 3. 向集合中添加数据 (文档)
    # Chroma 默认会在本地下载一个很小的开源嵌入模型 (all-MiniLM-L6-v2) 来把文本自动转成向量。
    print("正在向数据库中添加文档数据 (首次运行可能会自动下载轻量级默认模型，请耐心等待)...")
    collection.add(
        documents=[
            "草莓是一种非常甜美的水果，富含维生素C。",
            "人工智能（AI）正在改变我们的工作和生活方式。",
            "今天的天气非常适合去户外爬山。",
            "香蕉是猴子最喜欢吃的食物。",
            "深度学习是大语言模型的核心技术。"
        ],
        # 我们可以给每条文档附带一些元数据（比如出处、作者等），方便后期过滤
        metadatas=[
            {"category": "fruit"}, 
            {"category": "tech"}, 
            {"category": "weather"}, 
            {"category": "fruit"},
            {"category": "tech"}
        ],
        # 每条文档需要有一个唯一的 ID
        ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
    )
    print("文档添加成功！")

    # 4. 查询数据
    # 输入一个查询语句，Chroma 会找到语义上最相关的文档
    query_text = "有什么好吃的水果？"
    print(f"\n开始查询: '{query_text}'")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=2 # 表示返回最相关的前 2 个文档
    )

    print("\n--- 查询结果 ---")
    # results 会返回 ids, distances (距离/匹配度), metadatas 和 documents
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        # distance 越小通常代表越相似
        distance = results['distances'][0][i] 
        print(f"[{i+1}] 匹配到的文档: {doc} (类别: {meta['category']}, 距离: {distance:.4f})")
        
    # 我们再来查一个关于科技的
    query_text_2 = "机器学习是什么？"
    print(f"\n开始第二次查询: '{query_text_2}'")
    results_2 = collection.query(
        query_texts=[query_text_2],
        n_results=2 
    )
    print("\n--- 第二次查询结果 ---")
    for i in range(len(results_2['documents'][0])):
        doc = results_2['documents'][0][i]
        print(f"[{i+1}] 匹配到的文档: {doc}")

if __name__ == "__main__":
    main()

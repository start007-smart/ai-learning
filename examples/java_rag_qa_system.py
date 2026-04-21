import os
import sys
import chromadb

# 添加上一级目录到 sys.path，以便导入我们核心的 ai_client.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_client import AIClient

# =========================================================
# 这是一个完整的 RAG (检索增强生成) 系统的 Mini 版。
# 主要流程分两步：
# 1. 召回 (Retrieve): 用户提问 -> 去 ChromaDB 查找最相关知识段落
# 2. 生成 (Generate): 将找到的段落当成"小抄"交给大模型 -> 让大模型总结回答
# =========================================================

# 测试用的“内部私有”知识库数据
JAVA_KNOWLEDGE_DOCS = [
    "【JVM 垃圾回收】G1（Garbage-First）垃圾收集器在并发标记阶段使用的是 SATB（Snapshot-At-The-Beginning）算法，可以有效防止并发时存活对象被错误回收的问题。",
    "【Spring Boot】自动配置的核心原理是基于 @EnableAutoConfiguration。它会利用 SpringFactoriesLoader 去加载各 jar 包下的 META-INF/spring.factories 文件中配置的自定义类。",
    "【Spring IoC】Spring 解决单例 Bean 的循环依赖（即 A 依赖 B，B 也依赖 A），核心是引入了『三级缓存机制』：一级存放完成品，二级存放半成品(提前暴露)，三级存放 ObjectFactory 实例工厂。",
    "【Java 并发】ConcurrentHashMap 在 JDK 1.8 中抛弃了原有的分段锁（Segment），转而全面使用了 CAS (Compare-And-Swap) + synchronized 的机制。它的锁粒度被降低成了仅锁住链表或红黑树的头节点，并发度更高。"
]

def init_chroma_db():
    print("正在初始化本地 ChromaDB 并构建知识库 (首次可能需下载模型)...")
    client = chromadb.Client()
    # 每次运行前清理一下，方便演示
    try:
        client.delete_collection("java_company_kb")
    except Exception:
        pass
        
    collection = client.create_collection("java_company_kb")
    
    # 把文本转化为向量存进去
    collection.add(
        documents=JAVA_KNOWLEDGE_DOCS,
        # 同时记录一些元数据，实战中这里会存放文章归属的 URL 等
        metadatas=[{"topic": "JVM"}, {"topic": "Spring"}, {"topic": "Spring"}, {"topic": "JUC"}],
        ids=["doc_1", "doc_2", "doc_3", "doc_4"]
    )
    print("构建完成！\n" + "-"*50)
    return collection

def rag_ask(collection, query: str):
    """标准的 RAG 问答流程"""
    print(f"\n🤵🏻 用户提问：{query}")
    
    # 第 1 步：检索最近邻知识
    print(f"🔍 步骤1：正在向量数据库中搜索有关 '{query}' 的内部资料...")
    results = collection.query(
        query_texts=[query],
        n_results=1  # 为了精准，我们只调取匹配度最高的 1 段
    )
    
    if not results['documents'][0]:
        print("未检索到相关内容。")
        return
        
    context = results['documents'][0][0]
    distance = results['distances'][0][0]
    print(f"✅ 找到参考知识 (关联距离: {distance:.4f}):\n   >> {context}\n")
    
    # 距离过大（> 1.5），一般来说说明文本不相关（依据所用嵌入模型而定）
    # 但由于我们这里只是演示，不去严格阻断它。

    # 第 2 步：构建含有小抄的究极 Prompt，防止大模型发生幻觉（胡说八道）
    system_prompt = """你是一个严谨的 Java 企业级问答机器人。
【严厉指令】：请你严格且只根据下面的【参考背景资料】来回答用户的提问。
如果资料中没有直接涉及答案，请直接回复“抱歉，在本地知识库中未找到关于此问题的资料。”
绝不允许调用你自身脑海里已有的知识去编造！"""

    user_prompt = f"""
【参考背景资料】：
{context}

----------
【用户提问】：
{query}
"""

    print("🧠 步骤2：正在将问题与大字报资料揉入 Prompt，祈求大模型思考出结论...")
    # 这里默认会走 config.py 里配置的模型（例如智谱或Deepseek）
    ai = AIClient() 
    
    # 这里也可以为了严谨，把 temperature 设成很低，减少思维跳跃
    answer = ai.chat(message=user_prompt, system=system_prompt, temperature=0.1)
    
    print("\n🎉 系统最终回复：")
    print("====================")
    print(answer)
    print("====================\n")

def main():
    # 建立库
    db_collection = init_chroma_db()
    
    # 【测试案例 1】：正常匹配库内的知识点
    rag_ask(db_collection, "Spring 到底是怎么解决循环依赖的机制？具体分成了几级？")
    
    # 【测试案例 2】：超纲问题。验证大模型是否服从“找不到资料就说不知道”的原则
    # 这里的向量检索可能会匹配到一个八竿子打不着的最优解，但到了大模型层面，大模型会发现那个知识与Redis无关。
    rag_ask(db_collection, "Redis 为什么这么快？")

if __name__ == "__main__":
    main()

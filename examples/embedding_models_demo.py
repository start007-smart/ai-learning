import os
import sys
import math

# 添加父目录到系统路径，以便导入通用配置
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from config import get_config
except ImportError:
    pass

def cosine_similarity(v1: list, v2: list) -> float:
    """计算两个向量的余弦相似度"""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

def explain_embedding_models():
    """
    梳理与对比主流的三大 Embedding 模型体系
    """
    print("\n" + "="*70)
    print("🧠 主流 Embedding 模型理解对比：text-embedding-ada-002 / BGE / M3E")
    print("="*70)
    
    info = """
【1】text-embedding-ada-002 (OpenAI)
--------------------------------------------------
- 维度：1536 维
- 特点：商用领域的基准模型。支持多语言，上下文长度可达 8191 tokens。
- 适用：不想折腾本地部署、直接调用 API 的生产系统。它的通用性非常强。
- 进阶：OpenAI 目前已经推出了 text-embedding-3-small (支持降维到512) 和 large 版本，性价比更高。

【2】M3E (Moka Massive Mixed Embedding)
--------------------------------------------------
- 维度：768 维 (m3e-base)
- 特点：国内优秀的开源中文嵌入模型。在中文领域一度长期制霸，针对各种中文任务进行了海量混合数据训练。
- 适用：全本地化部署，特别是专注于中文语境的 RAG（检索增强生成）项目。
- 调用方式：通常基于 HuggingFace / sentence-transformers 本地加载。

【3】BGE (BAAI General Embedding)
--------------------------------------------------
- 维度：768 维 (bge-base) / 1024 维 (bge-large)
- 特点：由智源研究院 (BAAI) 开源出的一系列模型。目前在中文甚至多语言的 MTEB 榜单上常年霸榜，甚至超越了 text-embedding-ada-002。
- 适用：追求极致检索准确率的本地化 RAG 架构。它对“查询到文档 (Query-to-Document)”的非对称检索做了特殊优化。
- 调用方式：同样基于 sentence-transformers 或使用专门的推理引擎（如 Xinference、Ollama）。
    """
    print(info)

def demo_zhipu_embedding(texts: list):
    """
    调用智谱 AI 的 API 来演示获取 Embedding 并比较相似度。
    智谱提供的 embedding-2 / embedding-3 模型，其功能和定位对标商业模型。
    """
    try:
        from zhipuai import ZhipuAI
        config = get_config("zhipu")
        client = ZhipuAI(api_key=config["api_key"])
        
        print("\n[实时演示] 使用 智谱 AI (embedding-3) 提取向量，并计算相似度:")
        vectors = []
        for text in texts:
            resp = client.embeddings.create(
                model="embedding-3", # 智谱最新的向量大模型，支持多语言
                input=text,
            )
            # 获取向量数组
            vec = resp.data[0].embedding
            vectors.append(vec)
            print(f" -> 文本: '{text}' => 获得 {len(vec)} 维向量")
            
        if len(vectors) >= 2:
            sim = cosine_similarity(vectors[0], vectors[1])
            print(f" => 余弦相似度计算结果: {sim:.4f}")
            
    except ImportError:
         print("❌ 未安装 zhipuai，跳过在线演示。")
    except Exception as e:
         print(f"❌ 智谱 API 调用失败可能因未配置 Key，忽略演示。(Error: {e})")

def fake_local_embedding_code():
    """本地加载 BGE 或 M3E 模型的基础代码示例（仅作展示）"""
    print("\n" + "="*70)
    print("💻 本地开源模型 (BGE / M3E) 部署说明")
    print("="*70)
    tutorial = """如果你想在本地部署 M3E 或 BGE 模型（无需联网，数据绝对安全），
你需要安装 sentence-transformers 并运行以下代码：

```python
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer

# 1. 加载本地开源模型 (首次运行会从 HuggingFace/ModelScope 下载权重)
# model_name = "moka-ai/m3e-base"               # 加载 M3E
# model_name = "BAAI/bge-large-zh-v1.5"         # 加载 BGE
model = SentenceTransformer("BAAI/bge-large-zh-v1.5")

# 2. 从文本提取向量
sentences = ["什么是人工智能?", "机器学习是什么?"]
embeddings = model.encode(sentences)

print(f"向量维度: {len(embeddings[0])}")
```"""
    print(tutorial)

def main():
    # 1. 概念与理论对比
    explain_embedding_models()
    
    # 2. 本地化部署代码演示
    fake_local_embedding_code()
    
    # 3. 如果配置了 Zhipu Key 的话，使用真实 API 进行余弦相似度演示
    # 为了表现出“语义相似”和“字面相似”的区别：
    sample_texts = [
        "iPhone 15 Pro Max 的电池表现怎样？",
        "苹果最新旗舰手机的续航能力如何？" # 字面差异大，但语义高度相似
    ]
    demo_zhipu_embedding(sample_texts)
    
if __name__ == "__main__":
    main()

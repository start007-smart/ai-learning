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

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    使用 PyPDF2 解析 PDF 文件并提取文本内容。
    """
    try:
        import PyPDF2
    except ImportError:
        print("❌ 未安装 PyPDF2 库，请使用 pip install PyPDF2 安装。")
        sys.exit(1)

    print(f"📄 正在解析 PDF 文件: {pdf_path}")
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            print(f"-> 成功加载 PDF，共 {total_pages} 页。")
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                
                # 为了防止控制台输出过多信息，这里可以加上进度提示
                if (i + 1) % 10 == 0 or (i + 1) == total_pages:
                    print(f"-> 已解析 {i + 1}/{total_pages} 页")
    except FileNotFoundError:
        print(f"❌ 找不到文件: {pdf_path}。请检查路径。")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 解析 PDF 时出现错误: {e}")
        sys.exit(1)
        
    print(f"✅ 解析完成！共提取到 {len(text)} 个字符。")
    return text

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list:
    """
    按字符长度进行滑动窗口分块（Text Chunking）。
    实际开发中，还可以配合 tiktoken 按 Token 数分块，这里为了简单起见采用按字符数。
    
    Args:
        text: 提取的全部文本
        chunk_size: 每个 chunk 的最大字符数
        overlap: 相邻 chunk 之间的重叠字符数，以防从中间截断关键语义信息
    Returns:
        分块后的文本列表
    """
    print(f"\n✂️ 正在进行文本分块 (Chunk Size={chunk_size}, Overlap={overlap})...")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start += (chunk_size - overlap)
    
    # 过滤掉空字符串块
    chunks = [c for c in chunks if c]
    print(f"✅ 分块完成！共分成 {len(chunks)} 个 Text Chunk。")
    return chunks

def generate_embeddings_for_chunks(chunks: list) -> list:
    """
    调用智谱 AI (embedding-3 模型) 生成文本的向量。
    """
    try:
        from zhipuai import ZhipuAI
    except ImportError:
        print("❌ 未安装 zhipuai，请运行 pip install zhipuai")
        return []

    config = get_config("zhipu")
    client = ZhipuAI(api_key=config["api_key"])
    
    print("\n🧠 正在调用智谱大模型生成向量 (Embeddings)...")
    vectors = []
    
    # 为了演示，只取前 5 个 Chunk 进行向量化，以免消耗太多 API 资源
    demo_chunks = chunks[:5]
    if len(chunks) > 5:
        print("⚠️ 提示: 为了演示及节约资源，仅向量化前 5 个 Chunk。实际场景可全部处理。")
        
    for i, chunk in enumerate(demo_chunks):
        try:
            resp = client.embeddings.create(
                model="embedding-3", 
                input=chunk
            )
            vec = resp.data[0].embedding
            vectors.append({"id": i, "text": chunk, "vector": vec})
            print(f" -> Chunk {i+1} 向量化成功: 维度 {len(vec)}")
        except Exception as e:
            print(f"❌ 向量化 Chunk {i+1} 时出错: {e}")
            
    return vectors

def retrieve_similar_chunk(query: str, vector_db: list):
    """
    模拟向量检索：将用户的 Query 转化为向量后，在向量库(vector_db)中寻找最相似的 Chunk。
    """
    print(f"\n🔍 模拟向量检索 (RAG 核心步骤), 查询问题: '{query}'")
    try:
        from zhipuai import ZhipuAI
        config = get_config("zhipu")
        client = ZhipuAI(api_key=config["api_key"])
        
        # 1. 向量化用户查询
        resp = client.embeddings.create(
            model="embedding-3", 
            input=query
        )
        query_vec = resp.data[0].embedding
        
        # 2. 计算余弦相似度
        best_match = None
        highest_sim = -1.0
        
        for item in vector_db:
            sim = cosine_similarity(query_vec, item["vector"])
            print(f" -> 与 Chunk {item['id']+1} 的相似度: {sim:.4f}")
            if sim > highest_sim:
                highest_sim = sim
                best_match = item
                
        # 3. 输出最相似的结果
        if best_match:
            print(f"\n🏆 检索到最相关的内容 (相似度 {highest_sim:.4f}):")
            print("=" * 50)
            print(best_match["text"])
            print("=" * 50)
            
    except Exception as e:
        print(f"❌ 检索时出错: {e}")

def main():
    print("=" * 60)
    print("📚 [DEMO] RAG: PDF电子书切块与向量化提取演示")
    print("=" * 60)
    
    # 模拟准备一个 PDF 文件。实际运行时可替换为真实的电子书路径
    sample_pdf = os.path.join(os.path.dirname(__file__), "sample_ebook.pdf")
    
    if not os.path.exists(sample_pdf):
        print("\n⚠️ 当前目录没有找名为 sample_ebook.pdf 的文件。")
        print("由于这是演示脚本，请先将你的一本电子书(重命名为 sample_ebook.pdf)放置在: ")
        print(f"👉 {sample_pdf} \n然后再运行此脚本。")
        print("\n或者你也可以直接在下面代码中修改 sample_pdf 的路径！\n")
        
        # 为了演示继续运行，我们可以造两段假文本替代
        print("--- ⬇️ 降级为直接使用假文本进行演示 ---")
        full_text = "这是一部分用来测试的虚拟文本。在这个示例中，假设我们成功从PDF解析出了这部分文本：\n\n人工智能是一种研究... 我们希望让机器拥有智能的判断。"
    else:
        # 第一步：提取 PDF 文本
        full_text = extract_text_from_pdf(sample_pdf)
    
    if not full_text.strip():
        print("❌ 提取到的文本为空，可能是扫描版图片 PDF，需要 OCR 支持。")
        return
    
    # 第二步：将这本电子书切分成多个 Chunk（切块）
    chunks = chunk_text(full_text, chunk_size=300, overlap=50)
    
    # 第三步：利用大模型 API 把 Chunks 转成高维向量 (Embeddings)
    # 存入到内存版的“向量数据库” (List)
    vector_db = generate_embeddings_for_chunks(chunks)
    
    if not vector_db:
        print("❌ 向量库生成失败或为空，退出演示。")
        return
        
    # 第四步：模拟向量检索（针对已经向量化的内容提问测试）
    print("\n💡 提示: 演示中你可结合 Chunk内容自定义提问。")
    test_query = "什么是人工智能？" # 你可以修改为真实语境下的问题
    retrieve_similar_chunk(test_query, vector_db)

if __name__ == "__main__":
    main()

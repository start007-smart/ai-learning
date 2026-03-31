import os
import sys

# 添加父目录到系统路径，以便导入模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def chunk_by_chars(text: str, chunk_size: int = 150, overlap: int = 20):
    """
    策略一：按字符长度分块 (滑动窗口)
    适用场景：简单的纯文本，对完整语义要求不苛刻的情况。
    优点：实现简单，计算速度快。
    缺点：容易把一个完整的句子截断。
    """
    print("\n" + "="*60)
    print(f"策略一：按字符数量分块 (块大小: {chunk_size}, 重叠度: {overlap})")
    print("="*60)
    
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += (chunk_size - overlap)
        
    for i, chunk in enumerate(chunks):
        print(f"\n--- 字符块 {i+1} [长度 {len(chunk)}] ---")
        print(chunk)
    return chunks

def chunk_by_tokens(text: str, chunk_size: int = 70, overlap: int = 10):
    """
    策略二：按 Token 数量分块
    适用场景：由于大模型是按 Token 计费且各模型有明确的上下文 Token 限制，
              这是最能精确控制 Token 消耗和满足上下文长度要求的分块方式。
    注意：这里使用 OpenAI 的 tiktoken 作为演示，不同模型厂商的 Tokenizer 实现可能略有差异，但数量级基本一致。
    """
    print("\n" + "="*60)
    print(f"策略二：按 Token 数量分块 (块大小: {chunk_size}, 重叠度: {overlap})")
    print("="*60)
    
    try:
        import tiktoken
        # cl100k_base 是 GPT-3.5/GPT-4 使用的编码
        encoding = tiktoken.get_encoding("cl100k_base")
    except ImportError:
        print("未安装 tiktoken 分词库，正在使用简单的字符进行模拟。")
        print("请运行: pip install tiktoken")
        return chunk_by_chars(text, chunk_size, overlap)
        
    tokens = encoding.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        # 将 Token 解码回文本
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        if end == len(tokens):
            break
        start += (chunk_size - overlap)
        
    for i, chunk in enumerate(chunks):
        print(f"\n--- Token块 {i+1} [包含 Token 数: {len(encoding.encode(chunk))}] ---")
        print(chunk)
    return chunks

def chunk_by_semantics(text: str):
    """
    策略三：按语义分块 (例如按段落结构 \n\n 或者标点符号)
    适用场景：需要保证每块文本的语义完整性，例如 RAG（检索增强生成）场景。
    优点：能最大程度保留完整语义，适合被向量化后检索。
    缺点：块与块之间的大小可能极度不均匀。
    """
    print("\n" + "="*60)
    print("策略三：按语义（自然段落）分块")
    print("="*60)
    
    # 简单的按双换行符（段落）进行初步分块
    paragraphs = text.split("\n\n")
    # 去除空白段落
    chunks = [p.strip() for p in paragraphs if p.strip()]
    
    for i, chunk in enumerate(chunks):
        print(f"\n--- 语义块 {i+1} [基于自然段落与断句] ---")
        print(chunk)
    return chunks

def main():
    sample_text = """
人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。

人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

从诞生以来，理论和技术日益成熟，应用领域也不断扩大，可以设想，未来人工智能带来的科技产品，将会是人类智慧的“容器”。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

实际应用场景（如 RAG 系统）中的文本切分通常会结合多种策略：
比如先按自然段落划分（语义分块），如果某个段落依然超过了 Token 限制，
再对该段落内部按句子（。！？）进行二级切分；对于极端长句，最后使用精确的 Token 切分来兜底，这就是 LangChain 等框架里 RecursiveCharacterTextSplitter 的核心思想。
    """.strip()
    
    print("【示例文本内容】")
    print(sample_text)
    
    # 演示三种分块
    chunk_by_chars(sample_text, chunk_size=150, overlap=15)
    chunk_by_tokens(sample_text, chunk_size=80, overlap=10)
    chunk_by_semantics(sample_text)

if __name__ == "__main__":
    main()

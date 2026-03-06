"""
基础对话示例
"""

import sys
sys.path.append('..')

from ai_client import AIClient, quick_chat


def main():
    # 方式1: 快速对话
    print("=" * 50)
    print("方式1: 快速对话")
    print("=" * 50)
    response = quick_chat("Java中HashMap和ConcurrentHashMap的区别？")
    print(response)

    # 方式2: 使用客户端实例（推荐）
    print("\n" + "=" * 50)
    print("方式2: 客户端实例")
    print("=" * 50)

    client = AIClient(provider="zhipu")

    # 多轮对话模拟
    conversation = [
        "什么是JVM内存模型？",
        "堆和栈有什么区别？",
        "怎么排查内存泄漏？"
    ]

    for i, msg in enumerate(conversation, 1):
        print(f"\n--- 对话 {i} ---")
        print(f"Q: {msg}")
        response = client.chat(msg)
        print(f"A: {response[:200]}...")


if __name__ == "__main__":
    main()
"""
对比不同厂商的模型效果
"""

import sys
sys.path.append('..')

from ai_client import AIClient


def compare_same_prompt(prompt: str):
    """用相同Prompt测试不同模型"""

    providers = ["zhipu", "kimi", "deepseek"]

    print(f"📝 测试Prompt: {prompt}")
    print("=" * 80)

    for provider in providers:
        print(f"\n🤖 {provider.upper()}")
        print("-" * 80)
        try:
            client = AIClient(provider=provider)
            response = client.chat(prompt, temperature=0.7)
            print(response[:500])
        except Exception as e:
            print(f"❌ 错误: {e}")


def test_code_capability():
    """测试代码能力"""
    test_cases = [
        {
            "name": "Java基础",
            "prompt": "Java中 == 和 equals() 的区别？举例说明"
        },
        {
            "name": "并发编程",
            "prompt": "用Java写个生产者消费者模型，用BlockingQueue"
        },
        {
            "name": "性能优化",
            "prompt": "MySQL慢查询怎么排查？给出具体步骤和SQL"
        }
    ]

    for case in test_cases:
        print(f"\n{'='*80}")
        print(f"🧪 测试: {case['name']}")
        print(f"{'='*80}")
        compare_same_prompt(case['prompt'])


if __name__ == "__main__":
    print("🔬 模型对比测试\n")

    # 基础对比
    compare_same_prompt("解释什么是微服务架构，优缺点是什么？")

    # 代码能力对比
    print("\n\n" + "="*80)
    print("代码能力专项测试")
    print("="*80)
    test_code_capability()
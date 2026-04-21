"""
Prompt工程技巧演示
"""

import os
import sys

# 添加上一级目录到 sys.path，以便导入我们核心的 ai_client.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_client import AIClient


def compare_prompts():
    """对比不同Prompt的效果"""
    client = AIClient()

    topic = "Java中的异常处理"

    prompts = {
        "基础": f"解释{topic}",

        "结构化": f"""请解释{topic}，按以下格式：
        1. 核心概念（50字内）
        2. 使用场景（3个例子）
        3. 最佳实践（3条建议）
        4. 常见错误（2个反例）""",

        "角色扮演": f"""你是一位有10年经验的Java架构师，正在给初级工程师讲解{topic}。
        要求：
        - 用通俗易懂的语言
        - 结合实际项目经验
        - 给出可落地的建议""",

        "示例驱动": f"""解释{topic}，要求：
        - 先给出一个错误的代码示例
        - 解释为什么错
        - 给出正确的写法
        - 总结规律"""
    }

    for name, prompt in prompts.items():
        print(f"\n{'='*60}")
        print(f"📝 Prompt策略: {name}")
        print(f"{'='*60}")
        print(f"Prompt: {prompt[:80]}...")
        response = client.chat(prompt, temperature=0.5)
        print(f"Response: {response[:300]}...")


def few_shot_example():
    """Few-shot学习示例"""
    client = AIClient()

    # 不给示例
    print("=" * 60)
    print("❌ 零示例（Zero-shot）")
    print("=" * 60)
    prompt1 = "把以下中文转成蛇形命名: 用户订单数量"
    print(f"输入: {prompt1}")
    print(client.chat(prompt1))

    # 给示例
    print("\n" + "=" * 60)
    print("✅ 给示例（Few-shot）")
    print("=" * 60)
    prompt2 = """把中文转成蛇形命名（snake_case）:

    示例1:
    输入: 用户名称
    输出: user_name

    示例2:
    输入: 订单创建时间
    输出: order_create_time

    现在转换:
    输入: 用户订单数量
    输出:"""
    print(f"输入: {prompt2}")
    print(client.chat(prompt2))


def chain_of_thought():
    """思维链（Chain-of-Thought）"""
    client = AIClient()

    # 直接问
    print("=" * 60)
    print("❌ 直接问")
    print("=" * 60)
    q1 = "一个线程池核心线程数10，最大20，队列100。同时提交150个任务，有多少任务会拒绝？"
    print(f"Q: {q1}")
    print(client.chat(q1))

    # 分步思考
    print("\n" + "=" * 60)
    print("✅ 分步思考（CoT）")
    print("=" * 60)
    q2 = """一个线程池核心线程数10，最大20，队列100。同时提交150个任务，有多少任务会拒绝？

    请一步步思考：
    1. 先创建多少核心线程？
    2. 队列能容纳多少？
    3. 还能创建多少临时线程？
    4. 最后剩下多少任务？"""
    print(f"Q: {q2}")
    print(client.chat(q2))


if __name__ == "__main__":
    print("🎯 Prompt工程技巧演示\n")

    print("1. 对比不同Prompt策略")
    compare_prompts()

    print("\n\n2. Few-shot学习")
    few_shot_example()

    print("\n\n3. 思维链（CoT）")
    chain_of_thought()
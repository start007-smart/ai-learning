#!/usr/bin/env python3
"""
🚀 AI学习第一天 - 快速开始
运行: python demo.py
"""

import os
import sys
from dotenv import load_dotenv

# 提前加载 .env，确保 check_env() 能读取到 API Key
load_dotenv()


# 检查环境
def check_env():
    """检查API Key配置"""
    zhipu_key = os.getenv("ZHIPU_API_KEY", "")
    kimi_key = os.getenv("KIMI_API_KEY", "")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "")

    print("=" * 60)
    print("🔍 环境检查")
    print("=" * 60)

    if zhipu_key:
        print(f"✅ 智谱AI: 已配置 ({zhipu_key[:8]}...)")
    else:
        print("❌ 智谱AI: 未配置 (推荐，免费额度多)")

    if kimi_key:
        print(f"✅ Kimi: 已配置 ({kimi_key[:8]}...)")
    else:
        print("⚠️  Kimi: 未配置 (可选)")

    if deepseek_key:
        print(f"✅ DeepSeek: 已配置 ({deepseek_key[:8]}...)")
    else:
        print("⚠️  DeepSeek: 未配置 (可选)")

    if not any([zhipu_key, kimi_key, deepseek_key]):
        print("\n❌ 错误: 至少配置一个API Key!")
        print("请设置环境变量:")
        print("  export ZHIPU_API_KEY='your-key'")
        print("或创建 .env 文件")
        sys.exit(1)

    print("\n" + "=" * 60)

def main():
    check_env()

    from ai_client import AIClient

    # 使用默认厂商（在 config.py 中配置 DEFAULT_PROVIDER）
    from config import DEFAULT_PROVIDER
    print(f"🤖 初始化 {DEFAULT_PROVIDER} 客户端...")
    client = AIClient()


    # 场景1: 基础问答
    print("\n" + "=" * 60)
    print("💬 场景1: Spring Boot基础问答")
    print("=" * 60)
    question = "Spring Boot的自动配置原理是什么？请用3点说明。"
    print(f"Q: {question}")
    answer = client.chat(question)
    print(f"A: {answer}")

    # 场景2: 代码解释
    print("\n" + "=" * 60)
    print("💻 场景2: 代码解释")
    print("=" * 60)
    code = """
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Transactional
    public User createUser(String name) {
        User user = new User();
        user.setName(name);
        return userRepository.save(user);
    }
}
"""
    print("代码:")
    print(code)
    explanation = client.explain_code(code)
    print(f"\n解释:\n{explanation}")

    # 场景3: 代码审查
    print("\n" + "=" * 60)
    print("🔍 场景3: 代码审查")
    print("=" * 60)
    bad_code = """
public class Test {
    public static void main(String[] args) {
        for(int i=0; i<100; i++) {
            new Thread(() -> {
                System.out.println("Thread " + i);
            }).start();
        }
    }
}
"""
    print("问题代码:")
    print(bad_code)
    review = client.code_review(bad_code)
    print(f"\n审查结果:\n{review}")

    # 场景4: 代码生成
    print("\n" + "=" * 60)
    print("✨ 场景4: 代码生成")
    print("=" * 60)
    requirement = "写一个Java工具类，用JWT生成和验证Token，包含过期时间检查"
    print(f"需求: {requirement}")
    generated = client.generate_code(requirement)
    print(f"\n生成代码:\n{generated}")

    print("\n" + "=" * 60)
    print("🎉 所有演示完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 查看 examples/ 目录更多示例")
    print("2. 修改代码尝试不同Prompt")
    print("3. 实现自己的AI工具")

if __name__ == "__main__":
    main()
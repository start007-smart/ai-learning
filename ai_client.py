"""
统一AI客户端 - 支持智谱/Kimi/DeepSeek
"""

import os
import sys
from typing import List, Dict, Optional
from config import get_config, DEFAULT_PROVIDER


class AIClient:
    """统一的AI客户端，支持多厂商切换"""

    def __init__(self, provider: str = None, model: str = None):
        """
        初始化客户端

        Args:
            provider: 厂商名称 zhipu/kimi/deepseek
            model: 指定模型，None则使用默认
        """
        self.provider = provider or DEFAULT_PROVIDER
        self.config = get_config(self.provider)
        self.client = None
        self.model = model or self.config["model"]

        self._init_client()

    def _init_client(self):
        """初始化底层客户端"""
        if self.provider == "zhipu":
            try:
                from zhipuai import ZhipuAI
                self.client = ZhipuAI(api_key=self.config["api_key"])
            except ImportError:
                print("❌ 请先安装: pip install zhipuai")
                sys.exit(1)

        elif self.provider in ["kimi", "deepseek"]:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=self.config["api_key"],
                    base_url=self.config["base_url"]
                )
            except ImportError:
                print("❌ 请先安装: pip install openai")
                sys.exit(1)
        else:
            raise ValueError(f"不支持的厂商: {self.provider}")

        print(f"✅ 已初始化 [{self.provider}] 客户端，模型: {self.model}")

    def chat(self,
             message: str,
             system: str = "你是一位资深的Java开发专家，擅长Spring Boot、微服务架构和性能优化。",
             temperature: float = 0.7,
             stream: bool = False) -> str:
        """
        发送对话请求

        Args:
            message: 用户消息
            system: 系统提示词
            temperature: 创造性(0-2)，越低越确定
            stream: 是否流式返回

        Returns:
            AI回复内容
        """
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": message}
        ]

        try:
            if self.provider == "zhipu":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=stream
                )
                return response.choices[0].message.content

            else:  # kimi/deepseek 使用OpenAI格式
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=stream
                )
                return response.choices[0].message.content

        except Exception as e:
            return f"❌ 调用失败: {str(e)}"

    def code_review(self, code: str, language: str = "Java") -> str:
        """代码审查专用"""
        system = f"""你是一位严格的{language}代码审查专家。请分析代码并提供：
1. 潜在Bug和风险
2. 性能优化建议
3. 代码规范问题
4. 重构建议

格式：用Markdown列表输出，关键问题用⚠️标注。"""

        return self.chat(f"请审查以下代码：\n\n```{language.lower()}\n{code}\n```",
                        system=system,
                        temperature=0.3)

    def explain_code(self, code: str, level: str = "中级") -> str:
        """解释代码"""
        system = f"""你是一位耐心的编程导师，用{level}水平解释代码。
要求：
- 先概述功能
- 逐行解释关键逻辑
- 指出设计亮点
- 用类比帮助理解"""

        return self.chat(f"请解释这段代码：\n\n```java\n{code}\n```",
                        system=system)

    def generate_code(self, description: str, language: str = "Java") -> str:
        """生成代码"""
        system = f"""你是{language}专家，根据需求生成高质量代码。
要求：
- 包含必要的注释
- 考虑边界情况
- 使用最佳实践
- 只输出代码，不要解释"""

        return self.chat(f"需求：{description}\n\n请生成{language}代码：",
                        system=system,
                        temperature=0.5)


def quick_chat(message: str, provider: str = None) -> str:
    """快速对话，无需实例化"""
    client = AIClient(provider=provider)
    return client.chat(message)


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI客户端测试")
    print("=" * 50)

    # 测试基础对话
    client = AIClient()  # 默认用智谱

    print("\n1️⃣ 基础对话测试:")
    response = client.chat("什么是Spring Boot的自动配置？用一句话概括。")
    print(f"回答: {response[:100]}...")

    print("\n2️⃣ 代码解释测试:")
    code = """
    @RestController
    public class HelloController {
        @GetMapping("/hello")
        public String hello() {
            return "Hello World";
        }
    }
    """
    response = client.explain_code(code)
    print(f"解释: {response[:150]}...")

    print("\n✅ 测试完成！")
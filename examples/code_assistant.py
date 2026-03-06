"""
代码助手 - 你的AI编程伙伴
"""

import sys
sys.path.append('..')

from ai_client import AIClient


class CodeAssistant:
    def __init__(self):
        self.client = AIClient()

    def explain(self, code: str):
        """解释代码"""
        print("=" * 60)
        print("📖 代码解释")
        print("=" * 60)
        result = self.client.explain_code(code)
        print(result)

    def review(self, code: str):
        """审查代码"""
        print("=" * 60)
        print("🔍 代码审查")
        print("=" * 60)
        result = self.client.code_review(code)
        print(result)

    def optimize(self, code: str):
        """优化代码"""
        print("=" * 60)
        print("⚡ 代码优化")
        print("=" * 60)
        system = """你是Java性能优化专家。请：
1. 分析性能瓶颈
2. 给出优化后的代码
3. 解释优化原理"""
        result = self.client.chat(f"请优化以下代码：\n\n```java\n{code}\n```",
                                 system=system)
        print(result)

    def generate(self, requirement: str):
        """生成代码"""
        print("=" * 60)
        print("✨ 代码生成")
        print("=" * 60)
        result = self.client.generate_code(requirement)
        print(result)


def interactive_mode():
    """交互模式"""
    assistant = CodeAssistant()

    print("""
    🤖 Java代码助手
    命令:
      1 [代码] - 解释代码
      2 [代码] - 审查代码
      3 [代码] - 优化代码
      4 [需求] - 生成代码
      q - 退出
    """)

    while True:
        cmd = input("\n请输入命令: ").strip()

        if cmd == 'q':
            break
        elif cmd.startswith('1 '):
            assistant.explain(cmd[2:])
        elif cmd.startswith('2 '):
            assistant.review(cmd[2:])
        elif cmd.startswith('3 '):
            assistant.optimize(cmd[2:])
        elif cmd.startswith('4 '):
            assistant.generate(cmd[2:])
        else:
            print("未知命令")


if __name__ == "__main__":
    # 演示模式
    assistant = CodeAssistant()

    # 示例代码
    sample_code = """
    public List<User> getUsers() {
        List<User> users = new ArrayList<>();
        for(Long id : idList) {
            users.add(userDao.findById(id));
        }
        return users;
    }
    """

    assistant.explain(sample_code)
    print("\n")
    assistant.review(sample_code)
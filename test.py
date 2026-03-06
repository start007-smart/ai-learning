from ai_client import AIClient

# 创建客户端（默认智谱AI，免费）
client = AIClient()

# 基础对话
response = client.chat("解释Spring Boot自动配置原理")
print(response)

# 代码解释
code = "你的Java代码"
response = client.explain_code(code)

# 代码审查
response = client.code_review(code)

# 生成代码
response = client.generate_code("写一个JWT工具类")
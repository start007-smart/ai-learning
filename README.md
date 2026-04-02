# 🤖 AI Learning — 统一AI客户端学习库

> 面向 Java/后端开发者的 AI 编程入门实践项目，支持智谱 AI、Kimi、DeepSeek 三大厂商，开箱即用。

---

## ✨ 功能特性

- 🔌 **多厂商统一接口** — 一套代码，无缝切换智谱 AI / Kimi / DeepSeek
- 💬 **基础对话** — 支持自定义系统提示词、温度参数
- 📖 **代码解释** — 按指定水平（初级/中级/高级）解释代码逻辑
- 🔍 **代码审查** — 自动识别 Bug、性能问题及规范问题
- ✨ **代码生成** — 根据自然语言需求生成高质量代码
- 🔬 **模型对比** — 同一 Prompt 跨厂商横向对比效果
- 🎯 **Prompt 工程** — 结构化、Few-shot、思维链等技巧演示

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

在项目根目录创建 `.env` 文件（参考以下格式）：

```env
# 智谱 AI（推荐，免费额度多）
# 申请地址：https://open.bigmodel.cn/
ZHIPU_API_KEY=your_zhipu_api_key

# Kimi（可选）
# 申请地址：https://platform.moonshot.cn/
KIMI_API_KEY=your_kimi_api_key

# DeepSeek（可选）
# 申请地址：https://platform.deepseek.com/
DEEPSEEK_API_KEY=your_deepseek_api_key
```

> 💡 至少配置一个 API Key 即可运行。推荐使用 **智谱 AI**，免费额度充足，适合入门练习。

### 3. 运行 Demo

```bash
python demo.py
```

---

## 📁 目录结构

```
ai-learning/
├── .env                    # API Key 配置（本地，不提交 Git）
├── requirements.txt        # Python 依赖
├── config.py               # 厂商配置（模型名、Base URL）
├── ai_client.py            # 统一 AI 客户端核心类
├── demo.py                 # 🚀 快速入门演示（推荐从这里开始）
├── test.py                 # 基础调用示例
└── examples/               # 进阶示例
    ├── basic_chat.py           # 基础对话 & 多轮对话
    ├── code_assistant.py       # Java 代码助手（解释/审查/优化/生成）
    ├── compare_models.py       # 多厂商模型横向对比
    ├── prompt_engineering.py   # Prompt 工程技巧演示
    ├── java_to_python.py       # Java 代码 → Python 代码转换
    ├── generate_unit_test.py   # AI 自动生成 JUnit5 单元测试用例
    ├── mysql_query_demo.py     # MySQL 数据库连接与查询示例
    ├── function_calling_weather.py # AI Function Calling (函数调用) 示例
    ├── embedding_models_demo.py # 向量模型区别理解(ada-002/BGE/M3E)
    └── text_chunking.py        # 文本分块策略（按字符、Token、语义）
```

---

## 📦 支持的 AI 厂商

| 厂商 | 默认模型 | 特点 |
|------|----------|------|
| 智谱 AI | `glm-4-flash` | 免费额度多，适合入门 |
| Kimi | `moonshot-v1-8k` | 长上下文处理能力强 |
| DeepSeek | `deepseek-chat` | 代码能力突出，性价比高 |

---

## 🧩 核心用法

### 基础对话

```python
from ai_client import AIClient

client = AIClient()  # 默认使用智谱 AI
response = client.chat("解释 Spring Boot 自动配置原理")
print(response)
```

### 切换厂商

```python
# 使用 Kimi
client = AIClient(provider="kimi")

# 使用 DeepSeek
client = AIClient(provider="deepseek")
```

### 代码辅助

```python
# 解释代码
client.explain_code(code, level="中级")

# 代码审查（输出潜在 Bug、性能问题、规范建议）
client.code_review(code, language="Java")

# 生成代码
client.generate_code("写一个 JWT 工具类，包含过期时间检查")
```

### 快速调用（无需实例化）

```python
from ai_client import quick_chat

response = quick_chat("什么是微服务架构？")
print(response)
```

---

## 📚 示例说明

| 文件 | 说明 |
|------|------|
| `demo.py` | 入门首选，依次演示对话、解释、审查、生成四大场景 |
| `examples/basic_chat.py` | 快速对话与多轮对话示例 |
| `examples/code_assistant.py` | 交互式 Java 代码助手，支持命令行操作 |
| `examples/compare_models.py` | 同一问题让多个模型作答，方便横向对比 |
| `examples/prompt_engineering.py` | 演示结构化 Prompt、Few-shot 学习、思维链（CoT）技巧 |
| `examples/java_to_python.py` | 用 AI 将 Java 代码转换为地道的 Python 代码（含差异说明）|
| `examples/generate_unit_test.py` | 用 AI 自动生成 JUnit5 单元测试，覆盖工具类/Service/业务逻辑 |
| `examples/mysql_query_demo.py` | 演示 Python 连接本地 MySQL 数据库并获取表结构和数据 |
| `examples/function_calling_weather.py` | 演示大模型工具调用 (Function Calling)，实现通过天气 API 问答 |
| `examples/embedding_models_demo.py` | 向量(Embedding)模型理解：对比 text-embedding-ada-002、BGE、M3E，兼顾智谱提取演示 |
| `examples/text_chunking.py` | 常用文本分块策略演示（按字符、按 Token、按语义） |

---

## ⚙️ 配置说明

`config.py` 中可修改默认厂商和模型：

```python
# 修改默认厂商
DEFAULT_PROVIDER = "zhipu"  # 可改为 "kimi" 或 "deepseek"

# 智谱 AI 付费版（效果更强）
"model_paid": "glm-4"
```

---

## 🛠️ 常见问题

**Q: 提示 `❌ 请先安装: pip install zhipuai`？**  
A: 执行 `pip install -r requirements.txt` 安装所有依赖。

**Q: 提示 `至少配置一个API Key`？**  
A: 检查 `.env` 文件是否存在，并确认 Key 已正确填写（不含多余空格）。

**Q: 如何只用某一个厂商，跳过其他 Key 的配置？**  
A: 只需配置你要用的那一个 Key，其他留空即可。运行时通过 `provider` 参数指定厂商。

---

## 📝 License

MIT
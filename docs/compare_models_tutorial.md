# 兵器谱排名：如何用 Python 一键横向评测多款大模型 (Kimi/智谱/DeepSeek)

当我们面临新项目选型时，往往在纠结用智谱、Kimi，还是爆火的 DeepSeek？很多人的评测方法是打开三个网页，手动复制粘贴同一个问题，看谁写得好。但这种方式对于代码任务来说太难以规模化了。

在 `compare_models.py` 示范中，我们利用 Python 可以并行的优势，设计了一套极简的模型评测跑分架构。

## 统一的接口层：万佛朝宗

虽然不同大模型属于不同的公司，但是绝大多数公司为了能无缝撬开 OpenAI 的生态护城河，在 API 格式上都选择了**完全兼容 OpenAI 的接入标准 `base_url` 模式**。

这就意味着，你在代码里只需要实例化一个标准的 Client，通过换变量，就能随意切模型拿数据：

```python
# 智谱的地址和模型名
p1 = { "api": "https://open.bigmodel.cn/api/paas/v4/", "model": "glm-4-flash" }

# DeepSeek的地址和模型名
p2 = { "api": "https://api.deepseek.com", "model": "deepseek-chat" }

# Kimi的地址和模型名
p3 = { "api": "https://api.moonshot.cn/v1", "model": "moonshot-v1-8k" }
```

## 设计评测维度

对于我们后端开发而言，跑分不仅看正确率。我们一般从三个维度提问比较：
1. **纯代码能力（算法题）**：比如手搓一个高并发状态下线程安全的单例模式。
2. **长文本逻辑**：塞进去一份业务描述，让它们按需输出数据库表结构设计。
3. **格式服从度**：强制要求模型“只能输出 JSON 数组，不能包含一点 Markdown 或废话解释”。

通过脚本将这三个问题并发投递给这三家模型并打印输出。你会很快得出结论：谁的代码最健壮？谁的话痨最严重？谁最适合用来做工程化里的纯内容处理！

---
*本文是个人学习大模型实战方向的小记，希望对准备入门 AI 开发的大家有所启发。*

> **感谢关注，我会持续更新，欢迎查看相关源码实现与学习记录：**  
> [https://github.com/start007-smart/ai-learning](https://github.com/start007-smart/ai-learning)

"""
Function Calling Demo - 让AI调用外部工具查天气

核心流程：
  第1步: 用户提问（比如"北京今天天气怎么样？"）
  第2步: AI分析问题，决定是否需要调用工具，并输出调用参数
  第3步: 我们的代码执行真正的工具函数（这里是模拟天气API）
  第4步: 把工具执行结果返回给AI
  第5步: AI根据工具结果，生成最终自然语言回答

支持厂商: DeepSeek（推荐）/ Kimi / 智谱GLM-4
"""

import sys
import json
import random

sys.path.append('..')
from config import get_config

# ============================================================
# 第一部分：定义"工具"的结构（Tool Schema）
# AI 通过这份描述来理解有哪些工具可用、参数是什么
# ============================================================

# 天气查询工具定义（遵循 OpenAI Function Calling 格式）
WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市的实时天气信息，包含温度、天气状况、湿度、风速等数据",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "要查询天气的城市名称，例如：北京、上海、广州"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位，celsius=摄氏度（默认），fahrenheit=华氏度"
                }
            },
            "required": ["city"]  # city 是必填参数
        }
    }
}

# 工具列表（可以注册多个工具）
TOOLS = [WEATHER_TOOL]


# ============================================================
# 第二部分：模拟天气工具的实际执行逻辑
# 真实场景中，这里会调用和风天气、OpenWeatherMap 等真实API
# ============================================================

def get_weather(city: str, unit: str = "celsius") -> dict:
    """
    模拟天气查询（实际项目中替换为真实天气API）

    Args:
        city: 城市名
        unit: 温度单位

    Returns:
        天气数据字典
    """ 
    # 模拟不同城市的天气数据，增加随机浮动让结果更真实
    city_weather_data = {
        "北京": {"condition": "晴", "temp_base": 12, "humidity": 35, "wind": "西北风3级"},
        "上海": {"condition": "多云", "temp_base": 18, "humidity": 68, "wind": "东南风2级"},
        "广州": {"condition": "小雨", "temp_base": 22, "humidity": 85, "wind": "南风1级"},
        "深圳": {"condition": "阴", "temp_base": 21, "humidity": 80, "wind": "东风2级"},
        "成都": {"condition": "阴转多云", "temp_base": 15, "humidity": 75, "wind": "微风"},
        "杭州": {"condition": "晴", "temp_base": 17, "humidity": 60, "wind": "东北风2级"},
        "武汉": {"condition": "多云", "temp_base": 14, "humidity": 65, "wind": "北风3级"},
        "西安": {"condition": "晴", "temp_base": 10, "humidity": 40, "wind": "西风3级"},
    }

    # 查找城市数据（不在列表里的城市用随机数据）
    data = city_weather_data.get(city, {
        "condition": random.choice(["晴", "多云", "阴", "小雨"]),
        "temp_base": random.randint(5, 30),
        "humidity": random.randint(30, 90),
        "wind": "微风"
    })

    # 计算温度（加上随机浮动±2度）
    temp_celsius = data["temp_base"] + random.randint(-2, 2)
    temp_fahrenheit = round(temp_celsius * 9 / 5 + 32, 1)

    # 根据请求的单位返回对应温度
    temp = temp_celsius if unit == "celsius" else temp_fahrenheit
    temp_unit = "°C" if unit == "celsius" else "°F"

    return {
        "city": city,
        "condition": data["condition"],
        "temperature": f"{temp}{temp_unit}",
        "humidity": f"{data['humidity']}%",
        "wind": data["wind"],
        "suggestion": _get_suggestion(data["condition"], temp_celsius),
        "update_time": "2026-03-09 17:30"
    }


def _get_suggestion(condition: str, temp: int) -> str:
    """根据天气状况生成出行建议"""
    suggestions = []
    if "雨" in condition:
        suggestions.append("记得带伞")
    if temp < 10:
        suggestions.append("天气寒冷，注意保暖")
    elif temp > 28:
        suggestions.append("天气炎热，注意防晒补水")
    if "风" in condition or "级" in condition:
        suggestions.append("风力较大，出行注意安全")
    return "，".join(suggestions) if suggestions else "天气适宜，适合外出"


# ============================================================
# 第三部分：工具调度器
# 根据 AI 返回的工具名称，路由到对应的 Python 函数
# ============================================================

def execute_tool(tool_name: str, tool_args: dict) -> str:
    """
    执行 AI 请求的工具，并返回 JSON 字符串结果

    Args:
        tool_name: 工具名称（来自AI的响应）
        tool_args: 工具参数（来自AI的响应）

    Returns:
        工具执行结果（JSON字符串）
    """
    print(f"\n🔧 执行工具: {tool_name}")
    print(f"   参数: {json.dumps(tool_args, ensure_ascii=False)}")

    if tool_name == "get_weather":
        result = get_weather(**tool_args)
        print(f"   结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return json.dumps(result, ensure_ascii=False)
    else:
        return json.dumps({"error": f"未知工具: {tool_name}"})


# ============================================================
# 第四部分：Function Calling 主流程
# 使用 OpenAI 格式的 API（DeepSeek/Kimi 兼容此格式）
# ============================================================

def run_function_calling_demo(user_question: str, provider: str = "zhipu"):
    """
    Function Calling 完整演示，支持 zhipu / deepseek / kimi 三个厂商

    Args:
        user_question: 用户的问题
        provider: 使用的AI厂商（zhipu/deepseek/kimi）
    """
    config = get_config(provider)
    model = config["model"]

    print(f"\n{'='*60}")
    print(f"🤖 使用模型: [{provider}] {model}")
    print(f"💬 用户提问: {user_question}")
    print(f"{'='*60}")

    # ------- 统一消息格式（三家厂商都兼容 OpenAI messages 格式）-------
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个智能天气助手。"
                "【重要规则】当用户询问任何城市的天气时，你必须调用 get_weather 工具获取数据，"
                "绝对不能凭空编造天气数据。拿到工具返回的数据后，再用自然语言给出友好的回答。"
            )
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    print("\n📡 第1轮: 发送给AI，让它判断是否需要调用工具...")

    # ------- 初始化客户端并发送第1轮请求 -------
    if provider == "zhipu":
        # 智谱AI：使用官方 zhipuai SDK（格式与OpenAI一致，但用自家客户端）
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=config["api_key"])
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )
    else:
        # DeepSeek / Kimi：使用 OpenAI 兼容格式
        from openai import OpenAI
        client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

    ai_message = response.choices[0].message
    finish_reason = response.choices[0].finish_reason

    print(f"   finish_reason: {finish_reason}")

    # ------- Agentic Loop：循环调用工具，直到AI返回最终答案 -------
    # 原因：部分模型（如GLM）不支持并行工具调用，会分多次逐个调用工具
    # 最多循环5次，防止意外死循环
    round_num = 1
    while finish_reason == "tool_calls" and ai_message.tool_calls and round_num <= 5:
        print(f"\n✅ 第{round_num}次工具调用（共 {len(ai_message.tool_calls)} 个）")

        # 把AI的工具调用消息转为标准字典（兼容智谱SDK，避免Pydantic对象报错）
        tool_calls_dict = [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                }
            }
            for tc in ai_message.tool_calls
        ]
        messages.append({
            "role": "assistant",
            "content": ai_message.content or "",
            "tool_calls": tool_calls_dict
        })

        # 执行本轮所有工具调用
        for tool_call in ai_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_result = execute_tool(tool_name, tool_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

        # 再次调用AI，让它决定是继续调工具还是给出最终答案
        round_num += 1
        print(f"\n📡 第{round_num}轮: 把工具结果返回给AI...")

        next_response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,    # 仍传入tools，让AI可以继续调用（如还需查其他城市）
        )
        ai_message = next_response.choices[0].message
        finish_reason = next_response.choices[0].finish_reason
        print(f"   finish_reason: {finish_reason}")

    # 循环结束，获取最终答案
    if finish_reason != "tool_calls":
        final_answer = ai_message.content
        if not (ai_message.tool_calls):
            print("\n💡 AI直接回答（无需调用工具）" if round_num == 1 else "")
    else:
        final_answer = "⚠️ 达到最大工具调用次数限制（5次），请尝试简化问题。"

    # ------- 输出最终结果 -------
    print(f"\n{'='*60}")
    print("🌟 最终回答:")
    print(f"{'='*60}")
    print(final_answer)
    print(f"{'='*60}\n")

    return final_answer


# ============================================================
# 第五部分：运行多个测试案例
# ============================================================

def main():
    """运行 Function Calling 演示"""

    print("🛠️  Function Calling Demo - AI 调用外部工具查天气")
    print("=" * 60)
    print("核心流程: 用户提问 → AI分析 → 调用工具 → AI整合结果 → 输出回答")
    print("=" * 60)

    # 选择厂商（三家都支持 Function Calling）
    # zhipu = 智谱GLM-4（免费额度多，推荐）
    # deepseek = DeepSeek（余额不足时不可用）
    # kimi = 月之暗面（余额不足时不可用）
    provider = "zhipu"

    # 测试用例列表
    test_questions = [
        "北京今天天气怎么样？需要带伞吗？",
        "上海和广州的天气，哪个城市更适合今天出去玩？",   # 多城市对比（触发多次工具调用）
        "天气好不好？",                                    # 没有城市，看AI如何处理
    ]

    # 只跑第一个用例做演示（避免消耗太多token）
    # 如需测试所有用例，把下面的 [0:1] 改成 [:]
    for question in test_questions[0:1]:
        run_function_calling_demo(question, provider=provider)

    # ------- 多工具调用示例（选跑）-------
    print("\n" + "=" * 60)
    print("🔥 进阶示例：同时查询两个城市（AI会调用工具两次）")
    print("=" * 60)
    run_function_calling_demo(
        "帮我查一下上海和成都的天气，我需要决定去哪个城市出差",
        provider=provider
    )


if __name__ == "__main__":
    main()

"""
AI客户端配置
使用方式：
1. 复制 .env.example 为 .env
2. 填入你的API Key
3. 运行代码
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
CONFIG = {
    "zhipu": {
        "api_key": os.getenv("ZHIPU_API_KEY", ""),
        "model": "glm-4-flash",  # 免费版
        "model_paid": "glm-4",   # 付费版（更强）
        "base_url": None,  # 智谱用官方SDK
    },
    "kimi": {
        "api_key": os.getenv("KIMI_API_KEY", ""),
        "model": "moonshot-v1-8k",
        "base_url": "https://api.moonshot.cn/v1",
    },
    "deepseek": {
        "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com",
    }
}

# 默认使用的厂商
DEFAULT_PROVIDER = "zhipu"
# DEFAULT_PROVIDER = "deepseek"
# DEFAULT_PROVIDER = "kimi"

def get_config(provider=None):
    """获取指定厂商配置"""
    provider = provider or DEFAULT_PROVIDER
    return CONFIG.get(provider, CONFIG[DEFAULT_PROVIDER])
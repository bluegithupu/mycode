import json
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(api_key="sk-ac431075ac6347eea455c180d4d59217", base_url="https://api.deepseek.com")

# 定义请求数据
request_data = {
    "model": "deepseek-gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
}

# 发送请求
response = client.post("/v1/chat/completions", json=request_data)

# 解析响应
response_data = response.json()
print(json.dumps(response_data, indent=2))

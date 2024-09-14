import requests

# 设置 API 密钥和请求数据
api_key = 'your_api_key_here'
request_data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
}

# 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 发送请求
response = requests.post('https://platform.deepseek.com/api/v1/chat/completions', json=request_data, headers=headers)

# 打印响应
print(response.json())

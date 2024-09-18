import json
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(api_key="sk-ac431075ac6347eea455c180d4d59217", base_url="https://api.deepseek.com")

# 定义要调用的函数
def my_function(param):
    return f"Function called with parameter: {param}"

# 调用对话 API，使用 Function Calling
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Call my_function with parameter 'test'."}
    ],
    tools=[{
        "type": "function",
        "function": {
            "name": "my_function",
            "description": "my_function",
            "parameters": {
                "type": "object",
                "properties": {
                    "param": {
                        "type": "string",
                        "description": "user parameter",
                    }
                },
                "required": ["param"]
            },
        }
    }],
    stream=False
)

print(response.choices[0].finish_reason)

message = response.choices[0].message

# 打印响应内容
print(message.content)

# 调用本地 my_function
if message.tool_calls:
    for tool_call in message.tool_calls:
        print(tool_call)
        if tool_call.function.name == 'my_function':  # 使用属性访问
            param_value = json.loads(tool_call.function.arguments)['param']  # 解析 JSON 字符串
            result = my_function(param_value)
            print(result)  # 打印 my_function 的返回值




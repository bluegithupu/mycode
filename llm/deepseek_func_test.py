import json
from openai import OpenAI

from llm import tools

def send_messages(messages):

    # print debug info IN
    print("\n" + "=" * 80)
    print("📥 Input Messages:")
    print("-" * 40)
    # for msg in messages:
    #     print(f"[{msg['role']}] {msg['content']}")
    print(messages)
    print("=" * 80)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools.tools
    )

    # 增加错误检查
    if not response.choices[0].message.content and not response.choices[0].message.tool_calls:
        print("警告: API 返回了空响应!")
        # 可以选择重试或使用默认响应
        return ChatCompletionMessage(content="抱歉,我暂时无法处理这个请求。")

    # print debug info OUT
    print("\n" + "=" * 80)
    print("📤 API Response:")
    print("-" * 40)
    print(f"Model: {response.model}")
    print(f"Usage: {response.usage}")
    print(f"Message: {response.choices[0].message}")
    print("=" * 80 + "\n")

    return response.choices[0].message


# 初始化 OpenAI 客户端
client = OpenAI(api_key="sk-cdjsim5KBne5thQJ2bF279E94fEa487aA347A7D85747Af10",
                base_url="https://api.rcouyi.com/v1")

# messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
# messages = [{"role": "user", "content": "(1 + 1) * 2 / 0 = ?"}]
messages = [{"role": "user", "content": "What is the name of the album with the most tracks?"}]
message = send_messages(messages) 
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)




messages.append({"role": "tool", "tool_call_id": tool.id, "content": tools.call_tool(tool.function.name, **json.loads(tool.function.arguments))})
message = send_messages(messages)
if message.content:  # 检查是否有内容
    print(f"Model>\t {message.content}")
else:
    print("错误: 模型没有返回文本响应")

import json
from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(api_key="sk-ac431075ac6347eea455c180d4d59217", base_url="https://api.deepseek.com")


def get_llm_response(prompt, model="deepseek-chat"):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content

print(get_llm_response("hello"))
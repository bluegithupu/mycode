import requests
import json
from typing import Union, List

# 全局变量
API_KEY = "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"  # 请替换为您的实际API密钥

def tavily_search(query):
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_images": False,
        "include_answer": False,
        "max_results": 5
    }
    
    headers = {
        "content-type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return f"Error: {response.status_code}, {response.text}"



def tavily_extract(urls: Union[str, List[str]]):
    extract_url = "https://api.tavily.com/extract"
    
    # 确保 urls 是一个列表
    if isinstance(urls, str):
        urls = [urls]
    
    payload = {
        "api_key": API_KEY,
        "urls": urls,
        "include_images": False,
        "summarize": True
    }
    
    headers = {
        "content-type": "application/json"
    }
    
    response = requests.post(extract_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return f"Error: {response.status_code}, {response.text}"

# 使用示例

# 提取示例
urls_to_extract = [
    "https://docs.tavily.com/docs/welcome"
]  # 您可以提供一个URL列表或单个URL字符串

extract_result = tavily_extract(urls_to_extract)
print("\n提取结果:")
print(json.dumps(extract_result, indent=2, ensure_ascii=False))

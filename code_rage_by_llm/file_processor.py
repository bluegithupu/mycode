import os
import hashlib
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.help import get_llm_response
from logger import logger  # 直接导入 logger 实例

def calculate_md5(content):
    return hashlib.md5(content.encode()).hexdigest()

def process_file(file_path, existing_info=None):
    start_time = time.time()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    md5 = calculate_md5(content)
    last_modified = os.path.getmtime(file_path)

    if existing_info and existing_info.get('md5') == md5:
        logger.info(f"文件未变化，使用现有索引: {file_path}")
        return existing_info

    logger.info(f"开始分析文件内容: {file_path}")
    llm_start = time.time()
    symbols = analyze_with_llm(content)
    logger.info(f"LLM分析耗时: {time.time() - llm_start:.2f}秒")

    logger.info(f"处理文件总耗时: {time.time() - start_time:.2f}秒")

    return {
        "module_name": os.path.basename(file_path),
        "symbols": symbols,
        "last_modified": last_modified,
        "md5": md5
    }

def analyze_with_llm(content):
    prompt = f"""
    请分析以下代码文件，提取如下信息：
    - 用途
    - 函数列表
    - 变量列表
    - 类列表
    - 导入语句
    以下是代码内容：
    {content}
    """

    response = get_llm_response(prompt)
    return response.strip()
import os
import hashlib
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.help import get_llm_response
from logger import logger  # 直接导入 logger 实例

def calculate_md5(content):
    return hashlib.md5(content.encode()).hexdigest()

def process_file(file_path, existing_info=None, repo_content=None):
    start_time = time.time()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    md5 = calculate_md5(content)
    last_modified = os.path.getmtime(file_path)

    # if existing_info and existing_info.get('md5') == md5:
    #     logger.info(f"文件未变化，使用现有索引: {file_path}")
    #     return existing_info

    logger.info(f"开始分析文件内容: {file_path}")
    llm_start = time.time()
    symbols = analyze_with_llm(content)
    orientation = get_orientation(repo_content, content)
    logger.info(f"LLM分析耗时: {time.time() - llm_start:.2f}秒")

    logger.info(f"处理文件总耗时: {time.time() - start_time:.2f}秒")

    return {
        "module_name": os.path.basename(file_path),
        "symbols": symbols,
        "orientation": orientation,  # 添加 orientation 字段
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

def get_orientation(repo_content, file_content):
    prompt = f"""
    你是一个代码库分析专家。请分析以下信息：

    <代码仓库概览>
    {repo_content}
    </代码仓库概览>

    现在，我们需要确定以下文件在整个代码仓库中的作用和定位：

    <目标文件>
    {file_content}
    </目标文件>

    请提供一个简洁的描述，说明这个文件在整个代码仓库中的作用、重要性和与其他文件的关系。考虑以下几点：

    1. 文件的主要功能
    2. 文件与仓库其他部分的交互
    3. 文件在项目架构中的位置
    4. 文件对整个项目的贡献

    请用一到两句话总结这个文件的定位，以便于在后续的代码搜索和理解中快速定位此文件的作用。只需提供简洁的描述，无需其他解释。
    """

    response = get_llm_response(prompt)
    print("==========orientation==========")
    print(response)
    print("==========orientation==========")
    return response.strip()
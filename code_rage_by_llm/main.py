import os
import json
import time
from directory_traversal import traverse_directory
from file_processor import process_file
from data_storage import save_to_json
from logger import logger  # 直接导入 logger 实例
import sys

def load_existing_index(index_file):
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_repo_content(repo_path):
    content = ""
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.py', '.md', '.txt')):  # 可以根据需要添加更多文件类型
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content += f.read() + "\n\n"
    return content

def main():
    start_time = time.time()

    repo_path = "/Users/mac/Desktop/gpt_test/code_rage_by_llm"
    index_file = "index.json"

    logger.info(f"开始加载现有索引数据")
    existing_index = load_existing_index(index_file)
    logger.info(f"加载索引数据耗时: {time.time() - start_time:.2f}秒")

    logger.info(f"开始获取仓库内容")
    repo_content = get_repo_content(repo_path)
    logger.info(f"获取仓库内容耗时: {time.time() - start_time:.2f}秒")

    new_index_data = {}

    logger.info(f"开始遍历目录")
    traverse_start = time.time()
    files = traverse_directory(repo_path)
    logger.info(f"遍历目录耗时: {time.time() - traverse_start:.2f}秒，共找到 {len(files)} 个文件")

    process_start = time.time()
    for file_path in files:
        try:
            existing_info = existing_index.get(file_path, {})
            file_info = process_file(file_path, existing_info, repo_content)
            new_index_data[file_path] = file_info
            logger.info(f"处理文件完成: {file_path}")
        except Exception as e:
            logger.error(f"处理文件出错 {file_path}: {str(e)}")

    logger.info(f"处理所有文件耗时: {time.time() - process_start:.2f}秒")

    save_start = time.time()
    save_to_json(new_index_data, index_file)
    logger.info(f"保存索引数据耗时: {time.time() - save_start:.2f}秒")

    logger.info(f"总耗时: {time.time() - start_time:.2f}秒")

if __name__ == "__main__":
    main()
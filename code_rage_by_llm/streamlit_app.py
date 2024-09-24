import streamlit as st
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.help import get_llm_response

def load_index(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_indices(indices):
    formatted = ""
    for file_path, info in indices.items():
        formatted += f"文件路径: {file_path}\n"
        formatted += f"定位: {info.get('orientation', '未知')}\n"
        symbols = info.get('symbols', {})
        if isinstance(symbols, str):
            formatted += f"符号信息: {symbols}\n\n"
        else:
            formatted += f"用途: {symbols.get('用途', '未知')}\n"
            formatted += f"函数列表: {', '.join(symbols.get('函数列表', []))}\n"
            formatted += f"变量列表: {', '.join(symbols.get('变量列表', []))}\n"
            formatted += f"类列表: {', '.join(symbols.get('类列表', []))}\n"
            formatted += f"导入语句: {', '.join(symbols.get('导入语句', []))}\n\n"
    return formatted

def get_answer(query, indices):
    prompt = f"""
    下面是已知文件以及对应的符号信息：

    {format_indices(indices)}

    用户的问题是：

    {query}

    现在，请根据用户的问题以及前面的文件和符号信息，寻找相关文件路径。如果没有找到，返回空即可。

    请严格遵循以下步骤：

    1. 识别特殊标记：
       - 查找query中的 `@` 符号，它后面的内容是用户关注的文件路径。
       - 查找query中的 `@@` 符号，它后面的内容是用户关注的符号（如函数名、类名、变量名）。

    2. 匹配文件路径：
       - 对于 `@` 标记，在indices中查找包含该路径的所有文件。
       - 路径匹配应该是部分匹配，因为用户可能只提供了路径的一部分。

    3. 匹配符号：
       - 对于 `@@` 标记，在indices中所有文件的符号信息中查找该符号。
       - 检查函数、类、变量等所有符号类型。

    4. 分析依赖关系：
       - 利用 "导入语句" 信息确定文件间的依赖关系。
       - 如果找到了相关文件，也包括与之直接相关的依赖文件。

    5. 考虑文件用途和定位：
       - 使用每个文件的 "用途" 和 "定位" 信息来判断其与查询的相关性。

    6. 构建结果：
       - 对于每个相关文件，创建一个TargetFile对象。
       - 在reason字段中，详细说明为什么这个文件与查询相关。

    7. 返回结果：
       - 将所有找到的TargetFile对象放入FileList中返回。
       - 如果没有找到相关文件，返回一个空的FileList。

    请确保结果的准确性和完整性，包括所有可能相关的文件。
    """

    response = get_llm_response(prompt)
    return response

def main():
    st.title("代码库索引查询系统")

    # 加载索引数据
    index_file = "index.json"
    indices = load_index(index_file)

    # 用户输入
    query = st.text_input("请输入您的问题：")

    if st.button("提交"):
        if query:
            answer = get_answer(query, indices)
            st.write("回答：")
            st.write(answer)
        else:
            st.write("请输入一个问题。")

if __name__ == "__main__":
    main()
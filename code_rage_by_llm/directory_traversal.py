import os

def traverse_directory(root_path):
    file_list = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(('.py', '.java', '.js', '.ts', '.cpp', '.c', '.h')):  # 可以根据需要添加更多文件类型
                file_list.append(os.path.join(root, file))
    return file_list
import os
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Dict, Set, Tuple
import json
from datetime import datetime
import difflib

class DirectoryState:
    def __init__(self):
        self.directory_hashes: Dict[str, Dict[str, str]] = {}
        self.file_contents: Dict[str, str] = {}  # 存储文件路径和内容的映射
    
    def read_file_content(self, filepath: str) -> str:
        """读取文件内容，如果是二进制文件则返回None"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            return None  # 二进制文件返回None
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return None

    def calculate_file_hash(self, filepath: str) -> str:
        """计算文件的MD5哈希值"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()

    def get_file_diff(self, filepath: str, old_content: str, new_content: str) -> str:
        """生成文件内容的差异对比"""
        if old_content is None or new_content is None:
            return "Binary file - content diff not available"
        
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f'{filepath} (before)',
            tofile=f'{filepath} (after)',
            lineterm=''
        )
        return ''.join(diff)

    def compare_directory_changes(self, directory: str, new_hashes: Dict[str, str]) -> Tuple[Set[str], Set[str], Set[str]]:
        """比较目录的变更情况
        返回: (新增文件集合, 删除文件集合, 修改文件集合)
        """
        old_hashes = self.directory_hashes.get(directory, {})
        old_files = set(old_hashes.keys())
        new_files = set(new_hashes.keys())
        
        added_files = new_files - old_files
        deleted_files = old_files - new_files
        existing_files = old_files & new_files
        
        modified_files = {
            f for f in existing_files
            if old_hashes[f] != new_hashes[f]
        }
        
        return added_files, deleted_files, modified_files

    def update_directory_hash(self, directory: str) -> None:
        """更新指定目录下所有文件的哈希值并显示变更对比"""
        new_hashes = {}
        new_contents = {}
        
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    new_hashes[filename] = self.calculate_file_hash(filepath)
                    new_contents[filepath] = self.read_file_content(filepath)
            
            # 如果这个目录之前有记录，则进行对比
            if directory in self.directory_hashes:
                added, deleted, modified = self.compare_directory_changes(directory, new_hashes)
                
                if added or deleted or modified:
                    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Changes detected in {directory}:")
                    
                    if added:
                        print("\nAdded files:")
                        for f in added:
                            filepath = os.path.join(directory, f)
                            content = new_contents[filepath]
                            print(f"  + {f}")
                            if content is not None:
                                print("Content:")
                                print(content)
                            else:
                                print("Binary file - content not shown")
                    
                    if deleted:
                        print("\nDeleted files:")
                        for f in deleted:
                            print(f"  - {f}")
                    
                    if modified:
                        print("\nModified files:")
                        for f in modified:
                            filepath = os.path.join(directory, f)
                            old_content = self.file_contents.get(filepath)
                            new_content = new_contents[filepath]
                            print(f"\n  * {f}")
                            print("Changes:")
                            print(self.get_file_diff(f, old_content, new_content))
            
            # 更新目录的哈希值记录和文件内容记录
            self.directory_hashes[directory] = new_hashes
            for filepath, content in new_contents.items():
                self.file_contents[filepath] = content
            
        except Exception as e:
            print(f"Error updating directory {directory}: {e}")

    def scan_directories(self, start_path: str) -> None:
        """扫描并更新所有目录的哈希值"""
        for root, dirs, files in os.walk(start_path):
            if files:  # 只处理包含文件的目录
                self.update_directory_hash(root)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, directory_state: DirectoryState):
        self.directory_state = directory_state

    def on_any_event(self, event):
        if event.is_directory:
            return
        
        # 获取发生变化的文件所在的目录
        directory = os.path.dirname(event.src_path)
        
        # 更新该目录的哈希值
        self.directory_state.update_directory_hash(directory)

def main():
    # 获取当前工作目录
    path = os.getcwd()
    
    # 初始化目录状态
    directory_state = DirectoryState()
    
    # 首次扫描所有目录
    print("Initial directory scan:")
    directory_state.scan_directories(path)
    
    # 设置文件系统监控
    event_handler = FileChangeHandler(directory_state)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    print(f"\nStarted monitoring directory: {path}")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")
    
    observer.join()

if __name__ == "__main__":
    main()

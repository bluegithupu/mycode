import os
from pathlib import Path

class FileReader:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def traverse_and_write(self, output_file):
        with open(output_file, 'w') as out:
            for root, dirs, files in os.walk(self.root_dir):
                # Mapping of file extensions to language names
                extension_to_language = {
                    '.py': 'python',
                    '.go': 'golang',
                    # Add other languages and extensions as needed
                }
                for file in files:
                    file_extension = Path(file).suffix
                    if file_extension in extension_to_language:
                        file_path = Path(root) / file
                        language = extension_to_language[file_extension]
                        out.write(f"File path: {file_path}\n```{language}\n")

                        with open(file_path, 'r') as f:
                            out.write(f.read())
                        out.write("\n```\n\n")
                    
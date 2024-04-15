import sys
import os
from file_reader import FileReader


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]
    output_file = root_directory.split('/')[-1] + '.txt'
    current_path = "/Users/mac/Desktop/gpt_test/mycode/"
    output_file = os.path.join(current_path, output_file)



    file_reader = FileReader(root_directory)
    file_reader.traverse_and_write(output_file)


if __name__ == "__main__":
    main()

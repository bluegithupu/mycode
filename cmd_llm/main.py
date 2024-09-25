import os
from openai import OpenAI
import pyperclip
from colorama import init, Fore
from dotenv import load_dotenv
import sys

# 初始化 colorama
init()

def get_bash_command(description):
    client = OpenAI(api_key="sk-ac431075ac6347eea455c180d4d59217", base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个 Bash 命令专家。根据用户的描述,生成相应的 Bash 命令。只返回可执行命令本身,不要有其他任何内容。"},
            {"role": "user", "content": description}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    print(Fore.CYAN + "欢迎使用 Bash 命令生成器!" + Fore.RESET)
    
    if len(sys.argv) > 1:
        user_input = ' '.join(sys.argv[1:])
    else:
        print(Fore.YELLOW + "请输入您想要执行的操作描述 (输入 'q' 退出):" + Fore.RESET)
        user_input = input(Fore.GREEN + "> " + Fore.RESET)

    if user_input.lower() == 'q':
        print(Fore.CYAN + "谢谢使用,再见!" + Fore.RESET)
        return

    bash_command = get_bash_command(user_input)
    print(Fore.MAGENTA + "生成的 Bash 命令:" + Fore.RESET)
    print(Fore.WHITE + bash_command + Fore.RESET)

    pyperclip.copy(bash_command)
    print(Fore.GREEN + "命令已复制到剪贴板!" + Fore.RESET)
    print(Fore.CYAN + "完成" + Fore.RESET)

if __name__ == "__main__":
    main()
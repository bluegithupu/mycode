from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput


# This is a list of files to add to the chat
fnames = ["./../aider_auto_code_test/main.py"]

model = Model("gemini/gemini-1.5-pro-latest",
              weak_model="gemini/gemini-1.5-pro-latest")

io = InputOutput(yes=True)

# Create a coder object
coder = Coder.create(main_model=model, fnames=fnames, io=io)

# # This will execute one instruction on those files and then return
# coder.run("make a script that prints hello world")

# # Send another instruction
# coder.run("make it say goodbye")


tasks = [
    "使用 fastapi, 添加端点 /hello should return 'hello world'",
    "添加端点 /healthz should return 'ok'"
]

for task in tasks:
    coder.run(task)
    # Add completion flag after running the task
    print(f"Task '{task}' completed.")



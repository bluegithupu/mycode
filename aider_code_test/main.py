from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput


# This is a list of files to add to the chat
fnames = ["greeting.py"]

model = Model("gemini/gemini-1.5-pro-latest",
              weak_model="gemini/gemini-1.5-pro-latest")

io = InputOutput(yes=True)

# Create a coder object
coder = Coder.create(main_model=model, fnames=fnames, io=io)

# # This will execute one instruction on those files and then return
# coder.run("make a script that prints hello world")

# # Send another instruction
# coder.run("make it say goodbye")


coder.run("修改greeting.py文件，使用 fastapi, 添加端点 /hello should return 'hello world'")

coder.run("修改greeting.py文件， 添加端点 /healthz should return 'ok'")
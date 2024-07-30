import json
import os
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput


# This is a list of files to add to the chat
fnames = ["/Users/mac/Desktop/woker_code/monitor/README_FOR_AI.md"]

model = Model("gemini/gemini-1.5-pro-latest",
              weak_model="gemini/gemini-1.5-pro-latest")

io = InputOutput(yes=True)

# Create a coder object
coder = Coder.create(main_model=model, fnames=fnames, io=io, auto_commits=False, verbose=True, map_tokens=0)

# # This will execute one instruction on those files and then return
# coder.run("make a script that prints hello world")

# # Send another instruction
# coder.run("make it say goodbye")


# Load tasks and their statuses from a JSON file
def load_tasks(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {
            "tasks": [
                "请添加任务",
            ],
            "statuses": {}
        }

# Save tasks and their statuses to a JSON file
def save_tasks(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

tasks_file = "tasks.json"
data = load_tasks(tasks_file)
tasks = data["tasks"]
statuses = data["statuses"]

for task in tasks:
    if statuses.get(task) == "completed":
        print(f"Task '{task}' already completed. Skipping.")
        continue

    try:
        coder.run(task)
        statuses[task] = "completed"
        print(f"Task '{task}' completed.")
    except Exception as e:
        statuses[task] = f"failed: {str(e)}"
        print(f"Task '{task}' failed with error: {str(e)}")

    # Save the updated statuses
    save_tasks(tasks_file, {"tasks": tasks, "statuses": statuses})



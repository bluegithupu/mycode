import json
import os
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput

# Load tasks and their statuses from a JSON file
def load_tasks(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return {int(k): v for k, v in data.items()}
    return {}

# Save tasks and their statuses to a JSON file
def save_tasks(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Process a single task
def process_task(model, io, task_info):
    task = task_info["task"]
    status = task_info["status"]
    fnames = task_info.get("fnames", [])

    if status == "completed":
        print(f"Task '{task}' already completed. Skipping.")
        return

    coder = Coder.create(main_model=model, fnames=fnames, io=io)

    try:
        result = coder.run(task)
        if "Commit" in result:
            task_info["status"] = "completed"
            print(f"Task '{task}' completed.")
        else:
            task_info["status"] = f"error: {result}"
            print(f"Task '{task}' failed with error: {result}")
    except Exception as e:
        task_info["status"] = f"failed: {str(e)}"
        print(f"Task '{task}' failed with error: {str(e)}")

# Main function to execute tasks
def main():
    tasks_file = "tasks.json"
    data = load_tasks(tasks_file)

    model = Model("deepseek/deepseek-coder",
                  weak_model="deepseek/deepseek-coder")
    io = InputOutput(yes=True)

    for task_id, task_info in data.items():
        process_task(model, io, task_info)
        save_tasks(tasks_file, data)

    print("All tasks completed.")

if __name__ == "__main__":
    main()
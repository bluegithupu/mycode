from aider.models import Model
from aider.io import InputOutput
from task import TaskManager

def main():
    tasks_file = "tasks.json"
    task_manager = TaskManager(tasks_file)
    print(f"Loaded {len(task_manager.tasks)} tasks.")

    model = Model(task_manager.metadata.get("model", "deepseek/deepseek-coder"))
    io = InputOutput(yes=True, chat_history_file="/Users/mac/Desktop/tmp/code_test/.aider.chat.history.md")
    test_cmd = task_manager.metadata.get("test_cmd", "")

    for task in task_manager.tasks.values():
        task_manager.process_task(task, model, io, test_cmd)
        task_manager.save_tasks()

    print("All tasks completed.")

if __name__ == "__main__":
    main()

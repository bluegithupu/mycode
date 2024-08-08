import os
from aider.models import Model
from aider.io import InputOutput
from task import TaskManager
from aider.coders import Coder

def main():
    tasks_file = "tasks.json"
    task_manager = TaskManager(tasks_file)
    print(f"Loaded {len(task_manager.tasks)} tasks.")

    model = Model(task_manager.metadata.model or "deepseek/deepseek-coder")
    chat_history_file = os.path.join(task_manager.metadata.repo_path ,".aider.chat.history.md")
    io = InputOutput(yes=True, chat_history_file=chat_history_file)
    test_cmd = task_manager.metadata.test_cmd or ""

    coder = Coder.create(main_model=model, fnames=[], io=io, auto_commits=True, test_cmd=test_cmd, auto_test=True)
    for task in task_manager.tasks.values():
        coder.fnames = task.fnames
        task_manager.process_task(task, coder)
        task_manager.save_tasks()

    print("All tasks completed.")

if __name__ == "__main__":
    main()

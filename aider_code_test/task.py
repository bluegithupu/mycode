import json
import os
from aider.coders import Coder
import git


class Task:
    def __init__(self, task_id, task, fnames, status=""):
        self.id = task_id
        self.task = task
        self.fnames = fnames
        self.status = status

    def to_dict(self):
        return {
            "task": self.task,
            "fnames": self.fnames,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, task_id, task_dict):
        return cls(task_id, task_dict["task"], task_dict["fnames"], task_dict["status"])


class TaskManager:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = {}
        self.metadata = {}
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.metadata = data.get("MetaData", {})
                tasks_data = data.get("Tasks", {})
                self.tasks = {int(k): Task.from_dict(k, v)
                              for k, v in tasks_data.items()}

    def save_tasks(self):
        data = {
            "MetaData": self.metadata,
            "Tasks": {str(k): v.to_dict() for k, v in self.tasks.items()}
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def process_task(self, task, model, io, test_cmd):
        if task.status == "completed":
            # print(f"Task '{task.task}' already completed. Skipping.")
            return

        print(f"Task '{task.task}'  start !!!!!!!!!!!!!!!!!!!!!!!!!.")
        coder = Coder.create(main_model=model, fnames=task.fnames,
                             io=io, auto_commits=True, test_cmd=test_cmd, auto_test=True)

        repo = git.Repo(search_parent_directories=True)
        try:
            coder.run(task.task)
            result = coder.done_messages
            print(f"Task '{task.task}' result: {result}")
            test_result = coder.test_outcome
            print(f"test outcome '{test_result}'")
            
            result_ok = any(msg.get('role') == 'assistant' and msg.get('content') == 'Ok.' for msg in result)
            test_ok = test_result is None or test_result is True
            
            if result_ok:
                if test_ok:
                    task.status = "completed"
                    print(f"Task '{task.task}' completed.")
                else:
                    # Rollback the commit
                    aider_commit = coder.last_aider_commit_hash
                    repo.git.reset('--hard', aider_commit)
                    task.status = f"error: test failed, changes rolled back"
                    print(f"Task '{task.task}' failed: test failed, changes rolled back")
            else:
                task.status = f"error: result not OK"
                print(f"Task '{task.task}' failed: result not OK")
        except Exception as e:
            task.status = f"failed: {str(e)}"
            print(f"Task '{task.task}' failed with error: {str(e)}")

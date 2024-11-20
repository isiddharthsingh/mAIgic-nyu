# task_manager.py
import json
import os

class TaskManager:
    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file
        self.tasks_data = self.load_tasks()
        self.task_counter = self.get_next_task_id()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as file:
                return json.load(file)
        return {"tasks": []}

    def get_next_task_id(self):
        if self.tasks_data["tasks"]:
            return max(task["task_id"] for task in self.tasks_data["tasks"]) + 1
        return 1

    def add_task(self, description, deadline):
        task = {
            "task_id": self.task_counter,
            "task": description,
            "deadline": deadline
        }
        self.tasks_data["tasks"].append(task)
        self.task_counter += 1
        self.save_tasks()

    def update_task(self, task_id, description=None, deadline=None):
        for task in self.tasks_data["tasks"]:
            if task["task_id"] == task_id:
                if description:
                    task["task"] = description
                if deadline:
                    task["deadline"] = deadline
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        self.tasks_data["tasks"] = [task for task in self.tasks_data["tasks"] if task["task_id"] != task_id]
        self.save_tasks()

    def save_tasks(self):
        with open(self.tasks_file, 'w') as file:
            json.dump(self.tasks_data, file, indent=2)
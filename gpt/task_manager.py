# task_manager.py
import json
import os
import string

class TaskManager:
    def __init__(self, tasks_file="tasks.json"):
        self.tasks_file = tasks_file
        self.tasks_data = self.load_tasks()
        self.task_counter = self.get_next_task_id()

    def load_tasks(self):
        """
        Loads tasks from the JSON file. If the file doesn't exist, initializes an empty task list.
        """
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as file:
                return json.load(file)
        return {"tasks": []}

    def get_next_task_id(self):
        """
        Determines the next task ID based on existing tasks.
        """
        if self.tasks_data["tasks"]:
            return max(task["task_id"] for task in self.tasks_data["tasks"]) + 1
        return 1

    def find_task(self, thread_id, description):
        """
        Finds a task within a specific thread by its description.
        Performs case-insensitive matching and ignores punctuation.
        """
        normalized_input = description.lower().translate(str.maketrans('', '', string.punctuation))
        
        for task in self.tasks_data["tasks"]:
            if task["thread_id"] == thread_id:
                normalized_task = task["task"].lower().translate(str.maketrans('', '', string.punctuation))
                if normalized_task == normalized_input:
                    return task
        return None

    def get_tasks_for_thread(self, thread_id):
        """
        Retrieves all tasks for a specific thread.
        Returns a formatted string listing all tasks and their deadlines.
        """
        tasks = [task for task in self.tasks_data["tasks"] if task["thread_id"] == thread_id]
        tasks_str = ""
        for task in tasks:
            tasks_str += f"Task ID: {task['task_id']}, Description: {task['task']}, Deadline: {task['deadline']}\n"
        return tasks_str.strip()

    def add_task(self, thread_id, description, deadline):
        """
        Adds a new task to the tasks list.
        """
        task = {
            "task_id": self.task_counter,
            "thread_id": thread_id,
            "task": description,
            "deadline": deadline
        }
        self.tasks_data["tasks"].append(task)
        self.task_counter += 1
        self.save_tasks()

    def update_task(self, task_id, description=None, deadline=None):
        """
        Updates an existing task's description and/or deadline.
        """
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
        """
        Deletes a task by task_id.
        """
        self.tasks_data["tasks"] = [task for task in self.tasks_data["tasks"] if task["task_id"] != task_id]
        self.save_tasks()

    def save_tasks(self):
        """
        Saves the current tasks list to the JSON file.
        """
        with open(self.tasks_file, 'w') as file:
            json.dump(self.tasks_data, file, indent=2)

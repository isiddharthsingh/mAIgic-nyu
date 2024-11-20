# context_manager.py
import json
import os

class ContextManager:
    def __init__(self, contexts_file="contexts.json"):
        self.contexts_file = contexts_file
        self.contexts_data = self.load_contexts()

    def load_contexts(self):
        """
        Loads contexts from the JSON file. If the file doesn't exist, initializes an empty context dictionary.
        """
        if os.path.exists(self.contexts_file):
            with open(self.contexts_file, 'r') as file:
                return json.load(file)
        return {"threads": {}}

    def save_contexts(self):
        """
        Saves the current contexts to the JSON file.
        """
        with open(self.contexts_file, 'w') as file:
            json.dump(self.contexts_data, file, indent=2)

    def add_or_update_context(self, thread_id, updated_context):
        """
        Adds a new thread context or updates an existing one with the updated context paragraph.
        """
        thread_key = str(thread_id)
        if thread_key not in self.contexts_data["threads"]:
            self.contexts_data["threads"][thread_key] = {
                "thread_id": thread_id,
                "context": updated_context
            }
        else:
            self.contexts_data["threads"][thread_key]["context"] = updated_context

        self.save_contexts()

    def get_context(self, thread_id):
        """
        Retrieves the current context paragraph for a given thread ID.
        """
        thread_key = str(thread_id)
        return self.contexts_data["threads"].get(thread_key, {}).get("context", "")
# context_manager.py
import json
import os

class ContextManager:
    def __init__(self, contexts_file="contexts.json"):
        self.contexts_file = contexts_file
        self.contexts_data = self.load_contexts()

    def load_contexts(self):
        if os.path.exists(self.contexts_file):
            with open(self.contexts_file, 'r') as file:
                return json.load(file)
        return {"threads": {}}

    def save_contexts(self):
        with open(self.contexts_file, 'w') as file:
            json.dump(self.contexts_data, file, indent=2)

    def add_or_update_context(self, thread_id, message, message_date, notes="Processed for tasks and deadlines"):
        # If the thread ID doesn't exist, create a new thread entry
        if str(thread_id) not in self.contexts_data["threads"]:
            self.contexts_data["threads"][str(thread_id)] = {
                "thread_id": thread_id,
                "messages": [],
                "summary": ""
            }
        
        # Add the new message to the thread's messages list
        self.contexts_data["threads"][str(thread_id)]["messages"].append({
            "date": message_date,
            "content": message,
            "notes": notes
        })

        # Update the thread summary with new information (could be more detailed based on use case)
        self.contexts_data["threads"][str(thread_id)]["summary"] = f"Updated on {message_date} with latest message."

        # Save the updated contexts
        self.save_contexts()
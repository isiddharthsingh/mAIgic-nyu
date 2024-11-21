import os
import openai
from dotenv import load_dotenv

load_dotenv()

class ChatGPTClient:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.model = model

    def get_updated_context(self, current_context, new_message, message_date, existing_tasks):
        """
        Sends the current context, existing tasks, and a new message to ChatGPT to obtain an updated context summary.
        """
        prompt = f"""
        Current context: {current_context}

        Existing tasks:
        {existing_tasks}

        New message received on {message_date}: {new_message}

        Please provide an updated context summary as a single paragraph that includes all prior information and the new message.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()

    def extract_tasks_from_message(self, message, message_date, existing_tasks):
        """
        Sends a message to ChatGPT to extract tasks and deadlines, considering existing tasks.
        """
        prompt = f"""
        Current tasks:
        {existing_tasks}

        Extract all tasks and deadlines from the following message as individual entries. 
        Each task should be listed separately with a specific deadline in the format:
        Task:
        - Description: <task description>
        - Deadline: <specific date in YYYY-MM-DD format>
        Dont remvove dates or deadline related to the task from the description. it can be in both deadline and description.
        
        Message date: {message_date}
        Message content: {message}

        The final response should be just a json. No introductory text or conclusion etc. Provide the tasks in a JSON array format, where each task is an object with "description" and "deadline" keys.
        Example:
        [
            {{
                "description": "Task description",
                "deadline": "2024-12-31"
            }}
        ]
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content.strip()

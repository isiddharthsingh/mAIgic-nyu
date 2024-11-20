# openai_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ChatGPTClient:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        # Initialize the OpenAI client with the API key
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.model = model

    def get_tasks_from_message(self, message, message_date):
        # Construct the prompt to extract tasks and deadlines
        prompt = f"""
        Extract all tasks and deadlines from the following message as individual entries. 
        Each task should be listed separately with a specific deadline in the format:
        Task:
        - Description: <task description>
        - Deadline: <specific date in YYYY-MM-DD format>
        
        Message date: {message_date}
        Message content: {message}
        """
        
        # Call the OpenAI API to get a response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Return the response content
        return response.choices[0].message.content
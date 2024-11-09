import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initial base prompt template
base_prompt = """
You are analyzing an email thread. Below is the existing context of tasks and deadlines in this thread:
{}

Current message received on {}:
{}

Please list any new tasks or updates in the format:

Task:
- Description: <task description>
- Deadline: <specific date in YYYY-MM-DD format>

Update the context with any modified tasks or new deadlines, and reference prior tasks if applicable.
If no new tasks or updates are found, respond with "No new tasks found."
"""

# JSON structure to hold task data for an email thread
task_data = {
    "thread_id": "unique_thread_id",
    "messages": []
}

# Function to process each message and update JSON
def process_thread_message(message, message_date, task_data):
    # Format the prompt with current task context and new message
    current_task_summary = json.dumps(task_data["messages"], indent=2)  # Pretty-print JSON for prompt clarity
    formatted_prompt = base_prompt.format(current_task_summary, message_date, message)
    
    # Call the OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": formatted_prompt}
        ]
    )
    
    # Parse and update the JSON with new tasks from the current message
    response_content = completion.choices[0].message.content
    new_message_data = {
        "message_id": len(task_data["messages"]) + 1,
        "date": message_date,
        "content": message,
        "tasks": response_content
    }
    task_data["messages"].append(new_message_data)  # Update JSON with new message data
    return response_content, task_data

# Example usage with multiple messages in a thread
message_1 = "Complete the project report by next Friday and schedule a team meeting by Tuesday."
message_date_1 = "2024-11-09"
response_1, task_data = process_thread_message(message_1, message_date_1, task_data)
print("Response 1:\n", response_1)

message_2 = "Reschedule the team meeting to Wednesday and ensure the report includes financial analysis."
message_date_2 = "2024-11-10"
response_2, task_data = process_thread_message(message_2, message_date_2, task_data)
print("\nResponse 2:\n", response_2)

# Output the JSON structure as a final record of the thread
print("\nFinal Task Data JSON:\n", json.dumps(task_data, indent=2))

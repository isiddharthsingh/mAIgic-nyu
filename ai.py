import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Paths to store tasks and contexts JSON files
tasks_file_path = "tasks.json"
contexts_file_path = "contexts.json"

# Define structures to hold tasks and contexts separately
tasks_data = {"tasks": []}
contexts_data = {"contexts": []}
task_counter = 1  # Counter to assign unique task IDs
message_counter = 1  # Counter to assign unique message IDs

# Function to parse and extract tasks from ChatGPT response content
def extract_tasks_from_response(response_content):
    global task_counter
    tasks = []
    for line in response_content.split("\n\n"):
        if line.startswith("Task:"):
            parts = line.split("\n")
            description = parts[1].split(": ")[1]
            deadline = parts[2].split(": ")[1]
            tasks.append({
                "task_id": task_counter,
                "task": description,
                "deadline": deadline
            })
            task_counter += 1
    return tasks

# Function to process each message and update tasks and contexts
def process_thread_message(message, message_date, tasks_data, contexts_data):
    global message_counter
    # Format the prompt with the current context and new message
    formatted_prompt = f"""
    Extract all tasks and deadlines from the following message as individual entries. 
    Each task should be listed separately with a specific deadline in the format:
    Task:
    - Description: <task description>
    - Deadline: <specific date in YYYY-MM-DD format>
    
    Message date: {message_date}
    Message content: {message}
    """
    
    # Call the OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": formatted_prompt}
        ]
    )
    
    # Extract tasks from response and add them to the tasks list
    response_content = completion.choices[0].message.content
    tasks = extract_tasks_from_response(response_content)
    tasks_data["tasks"].extend(tasks)  # Add tasks to tasks_data dictionary
    
    # Add context to the contexts list
    contexts_data["contexts"].append({
        "message_id": message_counter,
        "date": message_date,
        "content": message,
        "notes": "Processed for tasks and deadlines"
    })
    message_counter += 1

    return tasks_data, contexts_data

# Example usage with multiple messages in a thread
message_1 = "Complete the project report by next Friday and schedule a team meeting by Tuesday."
message_date_1 = "2024-11-09"
tasks_data, contexts_data = process_thread_message(message_1, message_date_1, tasks_data, contexts_data)

message_2 = "Reschedule the team meeting to Wednesday and ensure the report includes financial analysis."
message_date_2 = "2024-11-10"
tasks_data, contexts_data = process_thread_message(message_2, message_date_2, tasks_data, contexts_data)

# Save tasks and contexts data to separate JSON files
with open(tasks_file_path, 'w') as tasks_file:
    json.dump(tasks_data, tasks_file, indent=2)

with open(contexts_file_path, 'w') as contexts_file:
    json.dump(contexts_data, contexts_file, indent=2)
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Path to store the simplified tasks JSON file
json_file_path = "simplified_tasks.json"

# Define a structure to hold only tasks
simplified_tasks = {"tasks": []}
task_counter = 1  # Counter to assign unique task IDs

# Function to parse and extract tasks from ChatGPT response content
def extract_tasks_from_response(response_content):
    global task_counter  # Declare global here
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

# Function to process each message and update the simplified tasks JSON
def process_thread_message(message, message_date, simplified_tasks):
    # Format the prompt with current task context and new message
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
    
    # Extract tasks from response and update the simplified tasks list
    response_content = completion.choices[0].message.content
    tasks = extract_tasks_from_response(response_content)
    simplified_tasks["tasks"].extend(tasks)  # Append extracted tasks to simplified_tasks list

    return simplified_tasks

# Example usage with multiple messages in a thread
message_1 = "Complete the project report by next Friday and schedule a team meeting by Tuesday."
message_date_1 = "2024-11-09"
simplified_tasks = process_thread_message(message_1, message_date_1, simplified_tasks)

message_2 = "Reschedule the team meeting to Wednesday and ensure the report includes financial analysis."
message_date_2 = "2024-11-10"
simplified_tasks = process_thread_message(message_2, message_date_2, simplified_tasks)

# Save the final tasks list to JSON
with open(json_file_path, 'w') as file:
    json.dump(simplified_tasks, file, indent=2)

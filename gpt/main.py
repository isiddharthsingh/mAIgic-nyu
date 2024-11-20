# main.py
import json
from openai_client import ChatGPTClient
from task_manager import TaskManager
from context_manager import ContextManager

# Initialize clients and managers
chat_client = ChatGPTClient()
task_manager = TaskManager()
context_manager = ContextManager()

# Function to process a single message with a thread ID
def process_message(thread_id, message, message_date):
    # Get tasks from OpenAI API response
    response_content = chat_client.get_tasks_from_message(message, message_date)

    # Split response to get task details
    for line in response_content.split("\n\n"):
        if line.startswith("Task:"):
            parts = line.split("\n")
            description = parts[1].split(": ")[1]
            deadline = parts[2].split(": ")[1]
            task_manager.add_task(description, deadline)

    # Add or update context in the specified thread
    context_manager.add_or_update_context(thread_id, message, message_date)

# Function to handle JSON file input
def process_from_file(file_path):
    with open(file_path, 'r') as file:
        messages = json.load(file)  # Load the JSON data as a list of dictionaries
        for msg in messages:
            # Extract each field from the JSON message object
            thread_id = msg["thread_id"]
            message = msg["message"]
            message_date = msg["message_date"]
            # Process each message with its thread ID and date
            process_message(thread_id, message, message_date)

# Function to handle manual input
def process_manual_input():
    while True:
        thread_id = input("Enter the thread ID (or type 'exit' to quit): ")
        if thread_id.lower() == 'exit':
            break
        message = input("Enter a message: ")
        message_date = input("Enter the date for this message (YYYY-MM-DD): ")
        process_message(thread_id, message, message_date)

def main():
    # Choose input method
    choice = input("Choose input method:\n1. File\n2. Manual\nEnter choice (1 or 2): ")
    
    if choice == "1":
        file_path = input("Enter the path to the file with messages: ")
        process_from_file(file_path)
    elif choice == "2":
        process_manual_input()
    else:
        print("Invalid choice. Please restart the program and enter 1 or 2.")

# Run main() if this file is executed directly
if __name__ == "__main__":
    main()
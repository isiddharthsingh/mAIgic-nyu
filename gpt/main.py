import json
from openai_client import ChatGPTClient
from task_manager import TaskManager
from context_manager import ContextManager
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

chat_client = ChatGPTClient()
task_manager = TaskManager()
context_manager = ContextManager()

def parse_tasks(tasks_content):
    """
    Parses the tasks extracted by ChatGPT from the response content.
    Expects tasks in the following JSON array format:
    [
        {
            "description": "Task description",
            "deadline": "YYYY-MM-DD"
        }
    ]
    """

    if tasks_content.startswith("```json"):
        tasks_content = tasks_content[len("```json"):].strip()
    if tasks_content.endswith("```"):
        tasks_content = tasks_content[:-len("```")].strip()

    try:
        tasks = json.loads(tasks_content)
        if isinstance(tasks, list):
            return tasks
        else:
            logging.error("Tasks content is not a list.")
            return []
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed: {e}")
        logging.error(f"Tasks content received: {tasks_content}")
        return []

def process_message(thread_id, message, message_date):
    """
    Processes a single message:
    1. Updates the context for the thread.
    2. Extracts tasks from the message.
    3. Adds or updates tasks in the task manager.
    """
    try:
        current_context = context_manager.get_context(thread_id)
        
        existing_tasks = task_manager.get_tasks_for_thread(thread_id)
        
        updated_context = chat_client.get_updated_context(current_context, message, message_date, existing_tasks=existing_tasks)
        
        context_manager.add_or_update_context(thread_id, updated_context)
        logging.info(f"Context updated for thread {thread_id}.")
        
        tasks_content = chat_client.extract_tasks_from_message(message, message_date, existing_tasks=existing_tasks)
        
        logging.info(f"Extracted tasks content for thread {thread_id}: {tasks_content}")
        
        tasks = parse_tasks(tasks_content)
        
        for task in tasks:
            description = task.get("description")
            deadline = task.get("deadline")
            if not description or not deadline:
                logging.warning(f"Incomplete task information: {task}")
                continue
            
            existing_task = task_manager.find_task(thread_id, description)
            if existing_task:
                if existing_task["deadline"] != deadline:
                    task_manager.update_task(existing_task["task_id"], deadline=deadline)
                    logging.info(f"Updated task_id {existing_task['task_id']} with new deadline {deadline}.")
            else:
                task_manager.add_task(thread_id, description, deadline)
                logging.info(f"Added new task: {description} with deadline {deadline}.")

    except Exception as e:
        logging.error(f"Error processing message in thread {thread_id}: {e}")

def process_from_file(file_path):
    """
    Processes messages from a JSON file.
    The JSON file should contain a list of message objects with thread_id, message, and message_date.
    """
    with open(file_path, 'r') as file:
        try:
            messages = json.load(file)  
        except json.JSONDecodeError:
            logging.error("Error: The file is not a valid JSON.")
            return
        for msg in messages:
            try:
                thread_id = int(msg["thread_id"])
                message = msg["message"]
                message_date = msg["message_date"]
                process_message(thread_id, message, message_date)
            except (KeyError, ValueError) as e:
                logging.warning(f"Skipping invalid message entry: {msg} due to {e}")
                continue

def process_manual_input():
    """
    Processes messages entered manually by the user.
    """
    while True:
        thread_id_input = input("Enter the thread ID (numeric) (or type 'exit' to quit): ")
        if thread_id_input.lower() == 'exit':
            break
        try:
            thread_id = int(thread_id_input)  
        except ValueError:
            logging.warning("Invalid thread ID. Please enter a number.")
            continue

        message = input("Enter a message: ")
        message_date = input("Enter the date for this message (YYYY-MM-DD): ")
        process_message(thread_id, message, message_date)

def main():
    """
    The main function that prompts the user to choose the input method and processes accordingly.
    """
    choice = input("Choose input method:\n1. File\n2. Manual\nEnter choice (1 or 2): ")
    
    if choice == "1":
        file_path = input("Enter the path to the JSON file with messages: ")
        process_from_file(file_path)
    elif choice == "2":
        process_manual_input()
    else:
        logging.error("Invalid choice. Please restart the program and enter 1 or 2.")

if __name__ == "__main__":
    main()

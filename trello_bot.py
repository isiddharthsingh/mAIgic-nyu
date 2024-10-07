import os
import requests
from slack_sdk import WebClient
from slack_bolt import App
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Environment variables
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')
TRELLO_LIST_NAME = os.getenv('TRELLO_LIST_NAME')

# Initialize the Slack app (Bolt framework)
app = App(token=SLACK_BOT_TOKEN)

# Fetch Trello list ID for the "To Do" list
def get_trello_list_id():
    url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        lists = response.json()
        for lst in lists:
            if lst['name'].lower() == TRELLO_LIST_NAME.lower():
                return lst['id']
    raise Exception(f"Could not find list {TRELLO_LIST_NAME} on the board")

# Add a card to the "To Do" list in Trello
def add_card_to_trello(card_name):
    list_id = get_trello_list_id()
    url = f"https://api.trello.com/1/cards"
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': list_id,
        'name': card_name
    }
    response = requests.post(url, params=query)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add card to Trello: {response.status_code}, {response.text}")

# Fetch Trello cards from the "To Do" list
def get_trello_cards():
    list_id = get_trello_list_id()
    url = f"https://api.trello.com/1/lists/{list_id}/cards?key={TRELLO_API_KEY}&token={TRELLO_TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        cards = response.json()
        tasks = [card['name'] for card in cards]
        return tasks
    else:
        raise Exception(f"Failed to fetch tasks from Trello: {response.status_code}, {response.text}")

# Post a message to Slack channel
def post_to_slack(channel, message):
    slack_client = WebClient(token=SLACK_BOT_TOKEN)
    response = slack_client.chat_postMessage(channel=channel, text=message)
    return response

# Handle "add" message in Slack and add the task to Trello
@app.message(re.compile(r'add "(.*)" to my todo'))
def add_to_trello_task(message, say, context):
    # Extract the task from the message
    task_to_add = context['matches'][0]
    
    # Add the task to Trello
    try:
        added_card = add_card_to_trello(task_to_add)
        response_message = f"Added '{task_to_add}' to your Trello 'To Do' list."
    except Exception as e:
        response_message = f"Failed to add the task. Error: {e}"
    
    # Post the result back to Slack
    post_to_slack(message['channel'], response_message)

# Handle "show me todo" message in Slack to fetch tasks from Trello
@app.event("message")
def show_todo_tasks(body, say, event):
    # Ensure the message contains the proper text
    if 'text' in event and 'show me todo' in event['text'].lower():
        # Fetch tasks from Trello
        try:
            tasks = get_trello_cards()
            if tasks:
                task_list = "\n".join(tasks)
                response_message = f"Here are the 'To Do' tasks:\n{task_list}"
            else:
                response_message = "No tasks found in 'To Do'."
        except Exception as e:
            response_message = f"Failed to fetch tasks. Error: {e}"
        
        # Post the result back to Slack
        post_to_slack(event['channel'], response_message)

# Start the Slack Bolt app (to listen for events using Socket Mode)
if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

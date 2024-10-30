import os
from slack_sdk import WebClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Slack client
slack_token = os.getenv('SLACK_BOT_TOKEN')
slack_channel = os.getenv('SLACK_CHANNEL_ID')
client = WebClient(token=slack_token)

# Send a message to the channel
response = client.chat_postMessage(
    channel=slack_channel,
    text="Hello, this is a message from my bot!"
)
print(response)

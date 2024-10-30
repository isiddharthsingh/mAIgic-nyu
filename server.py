import os
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from slack_sdk import WebClient
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Gmail API scope
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Environment variables for Slack and Gmail
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL_ID')
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CLIENT_SECRET')  

# Initialize Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Variable to store the last processed email ID (in memory)
last_processed_email_id = None

# Function to authenticate Gmail
def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', GMAIL_SCOPES)
        logger.info("Loaded credentials from token.json.")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logger.info("Refreshed expired credentials.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_FILE, GMAIL_SCOPES)
            creds = flow.run_local_server(port=0)
            logger.info("Completed authentication flow and obtained new credentials.")
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            logger.info("Saved new credentials to token.json.")
    return build('gmail', 'v1', credentials=creds)

# Fetch new emails from Gmail
def fetch_new_emails(service):
    global last_processed_email_id  # Use the global variable
    try:
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
        messages = results.get('messages', [])

        if messages:
            newest_email = messages[0]
            email_id = newest_email['id']

            if email_id == last_processed_email_id:
                logger.info("No new emails to process.")
                return  # Exit if it's the same email

            # Update the last processed email ID
            last_processed_email_id = email_id
            logger.info(f"Processing new email with ID: {email_id}")

            # Fetch the email content
            msg = service.users().messages().get(userId='me', id=email_id).execute()
            headers = msg['payload']['headers']
            sender = next(header['value'] for header in headers if header['name'] == 'From')
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            
            logger.info(f"Email fetched - Sender: {sender}, Subject: {subject}")
            notify_slack(sender, subject)
        else:
            logger.info("No new emails found.")
    except Exception as e:
        logger.error(f"Error fetching new emails: {e}")

# Post a message to Slack when a new email is received
def notify_slack(sender, subject):
    try:
        message = f"New email received from {sender}: {subject}"
        response = slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        logger.info(f"Message posted to Slack: {response['ok']}")
    except Exception as e:
        logger.error(f"Error sending message to Slack: {e}")

# Main function to run the Gmail check and notify Slack
def check_gmail_and_notify():
    service = authenticate_gmail()
    fetch_new_emails(service)

# Run the script periodically to check for new emails
if __name__ == "__main__":
    while True:
        check_gmail_and_notify()
        time.sleep(30)  # Check for new emails every 30 seconds

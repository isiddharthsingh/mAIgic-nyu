import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CLIENT_SECRET')

class GmailNotifier:
    def __init__(self, google_credentials_file):
        self.google_credentials_file = google_credentials_file
        self.gmail_scopes = ['https://www.googleapis.com/auth/gmail.readonly']

    def authenticate_gmail(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.gmail_scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.google_credentials_file, self.gmail_scopes)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def fetch_new_emails(self):
        service = self.authenticate_gmail()
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
        messages = results.get('messages', [])

        if messages:
            newest_email = messages[0]
            email_id = newest_email['id']

            # Fetch the email content
            msg = service.users().messages().get(userId='me', id=email_id).execute()
            headers = msg['payload']['headers']
            sender = next(header['value'] for header in headers if header['name'] == 'From')
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')

            return sender, subject
        else:
            return None, None

if __name__ == "__main__":
    notifier = GmailNotifier(GOOGLE_CREDENTIALS_FILE)
    sender, subject = notifier.fetch_new_emails()
    if sender and subject:
        print(f"New email from {sender}: {subject}")
    else:
        print("No new emails found.")

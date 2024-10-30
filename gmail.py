import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the Google client secret file
google_client_secret_file = os.getenv('GOOGLE_CLIENT_SECRET')

# Now you can use this file in your Gmail API authentication flow
print(f"Google Client Secret File: {google_client_secret_file}")

# Example usage with Gmail API
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file(google_client_secret_file, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

# Run the authentication function
authenticate_gmail()
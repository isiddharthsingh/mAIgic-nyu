import unittest
from unittest.mock import patch, MagicMock
from notifier import GmailNotifier

class TestGmailNotifier(unittest.TestCase):

    @patch('notifier.GmailNotifier.authenticate_gmail')
    def test_fetch_new_emails(self, mock_authenticate_gmail):
        # Mock the Gmail API service
        mock_service = MagicMock()
        mock_authenticate_gmail.return_value = mock_service
        
        # Mock the response for listing messages
        mock_service.users().messages().list().execute.return_value = {
            'messages': [{'id': '123'}]
        }

        # Mock the response for getting a specific message
        mock_service.users().messages().get().execute.return_value = {
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'test@example.com'},
                    {'name': 'Subject', 'value': 'Test Email'}
                ]
            }
        }

        # Initialize the notifier and fetch emails
        notifier = GmailNotifier('dummy_credentials.json')
        sender, subject = notifier.fetch_new_emails()

        # Assertions
        self.assertEqual(sender, 'test@example.com')
        self.assertEqual(subject, 'Test Email')

if __name__ == "__main__":
    unittest.main()

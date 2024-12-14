import os
from unittest.mock import MagicMock, patch
import pytest
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.error import BoltError
from src.maigic_nyu.api import SlackApp  # Replace 'your_module_name' with the actual file name
from dotenv import load_dotenv

def test_slack_app_initialization():
    load_dotenv()
    """Test if the SlackApp initializes without errors."""

    # Mock handler
    mock_handler = MagicMock()

    try:
        slack_app = SlackApp(message_handler=mock_handler, bot_token=os.environ.get("SLACK_BOT_TOKEN"), app_token=os.environ.get("SLACK_APP_TOKEN"))
        assert isinstance(slack_app.app, App)
        assert isinstance(slack_app.socket, SocketModeHandler)
    except BoltError:
        pytest.fail("SlackApp initialization failed!")

@patch("slack_bolt.App.message")
def test_message_handler_registration(mock_message_decorator):
    """Test if the message handler is registered properly."""
    load_dotenv()
    mock_handler = MagicMock()

    # Initialize SlackApp
    slack_app = SlackApp(message_handler=mock_handler, bot_token=os.environ.get("SLACK_BOT_TOKEN"), app_token=os.environ.get("SLACK_APP_TOKEN"))

    # Ensure the decorator is called
    mock_message_decorator.assert_called_once()

def test_message_handler_execution():
    """Test if the custom message handler is executed when a message event occurs."""
    load_dotenv()

    def mock_handler(message, say):
        say(f"Handled message: {message['text']}")

    # Initialize SlackApp
    slack_app = SlackApp(message_handler=mock_handler, bot_token=os.environ.get("SLACK_BOT_TOKEN"), app_token=os.environ.get("SLACK_APP_TOKEN"))
    
    # Mock the say function
    mock_say = MagicMock()

    # Sample message
    test_message = {"user": "U123", "text": "Hello, Slack!"}

    # Simulate the message handler
    slack_app.handler(test_message, mock_say)

    # Assert that the say function was called with the correct message
    mock_say.assert_called_once_with("Handled message: Hello, Slack!")

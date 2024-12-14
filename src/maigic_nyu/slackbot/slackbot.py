import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.error import BoltError

class SlackApp:
    def __init__(self, message_handler, bot_token, app_token):
        # Attempts to initializes app with bot token and socket mode handler
        try:
            self.app = App(token=os.environ.get(bot_token))
            @self.app.message()
            def wrapped_handler(message, say):
                self.handler(message, say)

            self.handler = message_handler
            self.socket = SocketModeHandler(self.app, app_token)
        except BoltError as e:
            # Generally, this error arises if the "SLACK_BOT_TOKEN" is invalid
            print("Error initializing Slack App:", e)

    def run(self):
        self.socket.start()
    
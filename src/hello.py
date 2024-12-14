import os
from maigic_nyu.api import SlackApp
from dotenv import load_dotenv


# Example usage
def message_handler(message, say):
    say(f"Hey there <@{message['user']}>! I am responding to: {message['text']}")


def main() -> None:
    load_dotenv()
    app = SlackApp(
        message_handler=message_handler,
        bot_token=os.environ.get("SLACK_BOT_TOKEN"),
        app_token=os.environ["SLACK_APP_TOKEN"]
    )
    app.run()

if __name__ == "__main__":
    main()

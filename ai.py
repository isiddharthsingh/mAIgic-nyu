import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

message_content = """
Please identify any tasks and their corresponding deadlines from the following message. 
Respond with the task and deadline in a structured format like this:
Task: <task description>
Deadline: <deadline>

Message: 'Complete the project report by next Friday and schedule a meeting with the team by Tuesday.'
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",  
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message_content}
    ]
)

print(completion.choices[0].message.content)
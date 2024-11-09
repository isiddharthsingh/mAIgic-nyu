import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Improved prompt template to intelligently relate tasks and use specific dates
base_prompt = """
Please analyze the following message and identify any tasks along with their deadlines.
The date of this message is {}. Convert any relative deadlines (e.g., "next Friday") into specific dates based on this date.
If tasks are related, structure each task so that any subsequent related tasks clearly reference prior tasks. Use phrases like "Continue with..." or "Follow up on..." to establish relationships.

List each task and deadline as separate entries in this format:

Task 1:
- Description: <task description>
- Deadline: <specific date in YYYY-MM-DD format>

Task 2:
- Description: <task description, indicating it is related to Task 1 if applicable>
- Deadline: <specific date in YYYY-MM-DD format>

If there are no tasks or deadlines, respond with "No tasks found." 
If a task does not have a specific deadline, list it as "Deadline: None."

Message: '{}'
"""

# Function to get structured tasks and deadlines with intelligent referencing
def get_task_and_deadline(message, message_date):
    formatted_prompt = base_prompt.format(message_date, message)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": formatted_prompt}
        ]
    )
    return completion.choices[0].message.content

# Example usage
user_message = "Complete the project report by next Friday and then review it with the team by Tuesday."
message_date = "2024-11-09"  # Replace with the actual date of the message
response = get_task_and_deadline(user_message, message_date)
print(response)
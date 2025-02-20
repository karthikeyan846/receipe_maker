from openai import OpenAI  # Import the OpenAI library to interact with the OpenAI API
from dotenv import load_dotenv  # Import the load_dotenv function from the python-dotenv library
import os  # Import the os module to access environment variables

# Load environment variables
load_dotenv()

# Initialize the OpenAI client with base URL and API key from environment variables
cli = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),  # Base URL for the OpenAI API from environment variable
    api_key=os.getenv("OPENAI_API_KEY"),   # API key for authentication from environment variable
)

def chat_completion(messages, model):
    # Create a chat completion request to the OpenAI API
    response = cli.chat.completions.create(
        model=model,  # Specify the model to use for the completion
        messages=[  # Define the messages for the chat
            {
                "role": "system",  # System message to set the context
                "content": "You are a cooking expert. The user will provide the ingredients they have, and you will suggest a recipe using those ingredients."
            },
            {
                "role": "user",  # User message containing the input
                "content": messages  # The user's input message
            }
        ]
    )
    
    # Extract the content of the response message
    message_content = response.choices[0].message.content
    
    return message_content  # Return the content of the response
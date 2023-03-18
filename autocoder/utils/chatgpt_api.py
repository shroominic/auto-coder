from dotenv import load_dotenv
from os import getenv
import openai


load_dotenv()
openai.api_key = getenv("OPENAI_API_KEY")


class ChatGPTSession:
    """
    A session with the chatgpt api
    """

    def __init__(self, system_prompt: str):
        self.history = [
            {"role": "system", "content": system_prompt}
        ]
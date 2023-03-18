from dotenv import load_dotenv
from typing import List
from os import getenv
import openai


load_dotenv()
openai.api_key = getenv("OPENAI_API_KEY")


class ChatGPTSession:
    """ Session with the chatgpt api """

    def __init__(self, model: str = "gpt4", history: List[dict] = []):
        self.history = history
        self.model = model
        self.usage = 0
        
    def add_user(self, message: str):
        """ Add a user message to the session history"""
        msg = {"role": "user", "content": f"{message}"}
        self.history.append(msg)
    
    def add_system(self, message: str):
        """ Add a system message to the session history"""
        msg = {"role": "system", "content": message}
        self.history.append(msg)
    
    def get_response(self) -> str:
        """ Get response and add it to the session history """
        if self.history[-1]["role"] == "assistant":
            self.add_system_message("Continue your response...")

        message = self.generate()
        self.history.append(message)
        return message.content.strip()
    
    def generate(self, history=None, **kwargs):
        """ Generate a response using the chatgpt api """
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history if history else self.history,
            **kwargs
        )
        self.usage += completion.usage["total_tokens"]
        print(f"Usage: {self.usage}")
        return completion.choices[0].message
    
    def __repr__(self) -> str:
        return f"ChatGPTSession(model={self.model}, cost={self.usage * 0.00003})"

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class GPTConnector:
    def __init__(self):
        self.conversations = {}

    def get_messages(self, user_id, user_input):
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        self.conversations[user_id].append({"role": "user", "content": user_input})
        return self.conversations[user_id]

    def add_response(self, user_id, response):
        self.conversations[user_id].append({"role": "assistant", "content": response})

    def reset(self, user_id):
        self.conversations[user_id] = []

    def chat(self, user_id, user_input, system_prompt):
        messages = [{"role": "system", "content": system_prompt}]
        messages += self.get_messages(user_id, user_input)
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=2000
        )
        reply = response["choices"][0]["message"]["content"]
        self.add_response(user_id, reply)
        return reply

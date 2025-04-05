import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class GPTConnector:
   def __init__(self):
       self.conversations = {}
       self.client = OpenAI(api_key=api_key)
       
       if not api_key:
           print("WARNING: OPENAI_API_KEY not found in environment variables!")

   def get_messages(self, user_id, user_input):
       if user_id not in self.conversations:
           self.conversations[user_id] = []
       self.conversations[user_id].append({"role": "user", "content": user_input})
       return self.conversations[user_id]

   def add_response(self, user_id, response):
       self.conversations[user_id].append({"role": "assistant", "content": response})

   def reset(self, user_id):
       if user_id in self.conversations:
           self.conversations[user_id] = []
           
   def update_api_key(self):
       load_dotenv(override=True)
       new_api_key = os.getenv("OPENAI_API_KEY")
       self.client = OpenAI(api_key=new_api_key)
       
       if not new_api_key:
           print("WARNING: OPENAI_API_KEY not found in environment variables!")
       else:
           print("API key has been updated")

   def chat(self, user_id, user_input, system_prompt):
       try:
           messages = [{"role": "system", "content": system_prompt}]
           messages += self.get_messages(user_id, user_input)
           
           response = self.client.chat.completions.create(
               model="gpt-4-turbo-preview",  
               messages=messages,
               max_tokens=2000
           )
           
           reply = response.choices[0].message.content
           self.add_response(user_id, reply)
           return reply
       
       except Exception as e:    
           error_message = str(e)
           print(f"Error calling OpenAI API: {error_message}")
           return f"Error details: {error_message}"
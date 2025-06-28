from openai import OpenAI
from dotenv import load_dotenv
import os
import re
load_dotenv()
api_key_ = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    api_key= api_key_,
)

model = "deepseek/deepseek-r1"
stream = False  # or False
max_tokens = 512

chat_completion_res = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "you are a professional AI helper。",
        },
        {
            "role": "user",
            "content": "Hello, How are you",
        }
    ],
    stream=stream,
    max_tokens=max_tokens,
)

if stream:
    for chunk in chat_completion_res:
        print(chunk.choices[0].delta.content or "", end="")
else:
    respuesta = chat_completion_res.choices[0].message.content
    respuesta_limpia = re.sub(r"<think>.*?</think>", "", respuesta, flags=re.DOTALL).strip()
  
print(respuesta_limpia)
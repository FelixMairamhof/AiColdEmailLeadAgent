import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()
client.api_key = api_key

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a professional salesman who writes cold emails with great sales copy to companies. You will receive the firm name and the product to sell as input."},
        {
            "role": "user",
            "content": "Firm name: IoT Wizard\nProduct: Innovative IoT devices for your office"
        }
    ]
)

print(completion.choices[0].message)
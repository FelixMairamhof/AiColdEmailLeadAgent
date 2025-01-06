import os
from dotenv import load_dotenv
from openai import OpenAI
import resend
from pydantic import BaseModel, EmailStr

class SalesEmailRequest(BaseModel):
    company: str
    value: str
    email: EmailStr

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
resend_api_key = os.getenv('RESEND_API_KEY')

print("Loaded environment variables")

client = OpenAI()
client.api_key = openai_api_key
resend.api_key = resend_api_key

print("Initialized OpenAI and Resend clients")

# Create an instance of SalesEmailRequest
sales_email_request = SalesEmailRequest(
    company="IoT Wizard",
    value="Innovative IoT devices for your office",
    email="schauen.k@gmail.com"
)

print(f"Created SalesEmailRequest: {sales_email_request}")

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a professional salesman who writes cold emails with great sales copy to companies. "
                                      "You will receive the firm name and the product to sell as input."
                                      " Your response should include only the email subject and the HTML body. "
                                      "Do not include any additional comments or placeholders."
                                      "Use the provided email for contact."
                                      "The email should be professional and engaging."
                                      "The email should be tailored to the firm and the product."
                                      "The email should be modern designed and good looking."},
        {
            "role": "user",
            "content": f"Firm name: {sales_email_request.company}\nProduct: {sales_email_request.value}"
        }
    ]
)

print("Received completion from OpenAI")

# Extract the message content
message_content = completion.choices[0].message.content
print(f"Message content: {message_content}")

# Assuming the LLM response contains the subject and body in a structured format
# For simplicity, let's assume the response is structured as follows:
# Subject: <subject>
# <html_body>

lines = message_content.split('\n', 1)
subject = lines[0].replace('Subject: ', '')
html_body = lines[1]

print(f"Extracted subject: {subject}")
print(f"Extracted HTML body: {html_body}")

# Send the email using Resend API
r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": sales_email_request.email,
  "subject": subject,
  "html": html_body
})

print("Email sent successfully")
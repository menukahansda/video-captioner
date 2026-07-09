import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

print("API Key Loaded:", api_key is not None)

client=genai.Client(api_key=api_key)

def generate_text(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

if __name__=="__main__":
    reply=generate_text("Generate some rhyming word for light")
    print(reply)
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")

#print("API Key Loaded:", api_key is not None)
if api_key is None:
    raise ValueError("GEMINI_API_KEY not found.")

client=genai.Client(api_key=api_key)


def generate_text(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

def generate_video_summary(contents):
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
    )
    return response.text



# if __name__=="__main__":
#     reply=generate_text("Generate some rhyming word for light")
#     print(reply)
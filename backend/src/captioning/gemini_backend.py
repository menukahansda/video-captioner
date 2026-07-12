import os
import time
import random
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash"


def _call_with_retry(contents, retries: int = 3, base_delay: float = 2.0) -> str:
    """
    Calls the Gemini API, retrying on transient server errors (503) and
    rate limiting (429) with exponential backoff + jitter. Raises the
    last error if all retries are exhausted.
    """
    last_error = None
    for attempt in range(retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
            )
            return response.text
        except genai_errors.ServerError as e:
            last_error = e
        except genai_errors.ClientError as e:
            last_error = e
            if getattr(e, "code", None) != 429:
                raise  

        if attempt < retries:
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)

    raise last_error


def generate_text(prompt: str):
    return _call_with_retry(prompt)


def generate_video_summary(contents):
    return _call_with_retry(contents)


# if __name__=="__main__":
#     reply = generate_text("Generate some rhyming word for light")
#     print(reply)
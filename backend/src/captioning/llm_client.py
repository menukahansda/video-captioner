import os
from src.captioning.gemini_backend import (
    generate_text as gemini_generate_text,
    generate_video_summary as gemini_generate_video_summary,
)

DEFAULT_BACKEND="gemini"

def generate_text(prompt: str):
    if DEFAULT_BACKEND == "gemini":
        return gemini_generate_text(prompt)
    raise ValueError(
        f"Unsupported backend: {DEFAULT_BACKEND}"
    )

def generate_video_summary(contents):

    if DEFAULT_BACKEND == "gemini":
        return gemini_generate_video_summary(contents)

    raise ValueError(
        f"Unsupported backend: {DEFAULT_BACKEND}"
    )

# if __name__ == "__main__":

#     response = generate_text(
#         "Write one sentence about Artificial Intelligence."
#     )

#     print(response)
import os
from src.captioning.gemini_backend import (
    generate_text as gemini_generate_text,
    generate_video_summary as gemini_generate_video_summary,
)

from src.captioning.local_backend import (
    generate_text as local_generate_text,
    generate_video_summary as local_generate_video_summary,
)

DEFAULT_BACKEND = "gemini"

def generate_text(prompt: str):
    if DEFAULT_BACKEND == "gemini":
        return gemini_generate_text(prompt)

    elif DEFAULT_BACKEND == "local":
        return local_generate_text(prompt)

    raise ValueError(
        f"Unsupported backend: {DEFAULT_BACKEND}"
    )

def generate_video_summary(contents):
    if DEFAULT_BACKEND == "gemini":
        return gemini_generate_video_summary(contents)

    elif DEFAULT_BACKEND == "local":
        return local_generate_video_summary(contents)

    raise ValueError(
        f"Unsupported backend: {DEFAULT_BACKEND}"
    )

# if __name__ == "__main__":
#     from pathlib import Path
#     from PIL import Image

#     frame_dir = Path("data/frames/v1")

#     contents = [
#         "Describe these video frames in a concise factual summary."
#     ]

#     for image_path in sorted(frame_dir.glob("*.jpg")):
#         contents.append(Image.open(image_path))

#     summary = generate_video_summary(contents)

#     print(summary)
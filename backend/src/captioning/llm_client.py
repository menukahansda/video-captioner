import os
import re            
import json 

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

def _generate_video_summary_raw(contents):
    if DEFAULT_BACKEND == "gemini":
        return gemini_generate_video_summary(contents)

    elif DEFAULT_BACKEND == "local":
        return local_generate_video_summary(contents)

    raise ValueError(
        f"Unsupported backend: {DEFAULT_BACKEND}"
    )

def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    return json.loads(cleaned)

def generate_json(prompt: str, retries: int = 1) -> dict:
    last_error = None
    for attempt in range(retries + 1):
        raw = generate_text(prompt)
        try:
            return _extract_json(raw)
        except (json.JSONDecodeError, AttributeError) as e:
            last_error = e
            continue
    raise ValueError(f"Failed to get valid JSON after {retries + 1} attempts: {last_error}")

def generate_video_summary(contents, retries: int = 2) -> dict:
    last_error = None
    for attempt in range(retries + 1):
        raw = _generate_video_summary_raw(contents)
        try:
            return _extract_json(raw)
        except (json.JSONDecodeError, AttributeError) as e:
            last_error = e
            continue
    raise ValueError(f"Failed to get valid JSON after {retries + 1} attempts: {last_error}")

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
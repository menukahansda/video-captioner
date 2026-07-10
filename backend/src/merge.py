from PIL import Image
from src.captioning.prompts import(
    SYSTEM_PROMPT,
    VIDEO_UNDERSTANDING_PROMPT,
)

from src.captioning.llm_client import generate_video_summary

def summarize_video(frame_paths, transcript):
    """
    Generate a factual summary of a video using
    extracted keyframes and transcript.
    """

    contents = []

    prompt = f"""
{SYSTEM_PROMPT}

{VIDEO_UNDERSTANDING_PROMPT}
"""

    contents.append(prompt)

    for path in frame_paths:
        image = Image.open(path)
        contents.append(image)

    if transcript.strip():
        contents.append(f"Transcript:\n{transcript}")

    summary = generate_video_summary(contents)

    return summary


if __name__ == "__main__":
    from pathlib import Path

    frame_dir = Path("data/frames/v1")

    frame_paths = sorted(frame_dir.glob("*.jpg"))

    transcript = "No speech available."

    summary = summarize_video(frame_paths, transcript)

    print(summary)
from pathlib import Path
from PIL import Image

from src.captioning.gemini_backend import generate_video_summary
from src.captioning.prompts import (
    SYSTEM_PROMPT,
    VIDEO_UNDERSTANDING_PROMPT,
)
frame_dir = Path("data/frames/v1")
images=[]
for image_path in sorted(frame_dir.glob("*.jpg")):
    image = Image.open(image_path)
    images.append(image)

# print(images)
#Temporary transcript
transcript = "No speech available."

prompt=f"""
{SYSTEM_PROMPT}
{VIDEO_UNDERSTANDING_PROMPT}
You are provided with:
- Keyframes extracted from a video.
- A transcript generated from the video's audio.

Generate one concise, factual summary of the complete video.
If the transcript and visuals differ, prioritize the visual content.
Transcript:
{transcript}
"""
contents=[]
contents.append(prompt)
contents.extend(images)
contents.append(transcript)

try:
    summary = generate_video_summary(contents)
    print("\nVideo Summary\n")
    print(summary)
except Exception as e:
    print(f"Gemini Error: {e}")

finally:
    for image in images:
        image.close()
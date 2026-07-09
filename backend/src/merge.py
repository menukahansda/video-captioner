from PIL import Image
from src.captioning.prompts import(
    SYSTEM_PROMPT,
    VIDEO_UNDERSTANDING_PROMPT,
)

from src.captioning.gemini_backend import(
    generate_video_summary,
)

def summarize_video(frame_paths,transcript):
    contents=[]
    prompt=f"""
    {SYSTEM_PROMPT}
    {VIDEO_UNDERSTANDING_PROMPT}
    Transcript:
    {transcript}
    """
    contents.append(prompt)
    for path in frame_paths:
        contents.append(Image.open(path))
    
    if transcript.strip():
        contents.append(transcript)

    return generate_video_summary(contents)
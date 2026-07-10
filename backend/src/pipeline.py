from pathlib import Path

from config.settings import VIDEO_DIR

from src.preprocessing.validate import validate_video
from src.preprocessing.keyframe_extractor import extract_keyframes
from src.preprocessing.audio_extractor import extract_audio
from src.preprocessing.audio_transcribe import transcribe_audio
from src.merge import summarize_video
from src.captioning.caption_generator import generate_captions

def run_pipeline(video_path : str | Path, task_id : str, backend_name="gemini"):
    # 1. Validate input
    validate_video(video_path) 
    
    # 2. Extract
    frames = extract_keyframes(video_path, task_id)  
    audio = extract_audio(video_path, task_id)

    # 3. Transcribe 
    transcript = transcribe_audio(audio)

    # 4. Summary
    summary = summarize_video(frames, transcript)
    # 5. Generate Captions
    captions = generate_captions(summary)

    # 5.Return Final Output
    result = {
        "summary": summary,
        "captions": captions,
    }

    return result

if __name__ == "__main__":

    video_path = VIDEO_DIR / "examples" / "e1.mp4"

    result = run_pipeline(video_path)

    print("\n===== VIDEO SUMMARY =====\n")
    print(result["summary"])

    print("\n===== CAPTIONS =====\n")

    for style, caption in result["captions"].items():
        print(f"{style}:")
        print(caption)
        print()
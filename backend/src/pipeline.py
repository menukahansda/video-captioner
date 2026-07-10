from pathlib import Path

from config.settings import VIDEO_DIR

from src.preprocessing.validate import validate_video
from src.preprocessing.keyframe_extractor import extract_keyframes
from src.preprocessing.audio_extractor import extract_audio
from src.preprocessing.audio_transcribe import transcribe_audio

def run_pipeline(video_path : str | Path, backend_name="gemini", config=None):
    # 1. Validate input
    validate_video(video_path) 
    
    # 2. Extract
    task_id = Path(video_path).stem
    frames = extract_keyframes(video_path, task_id)  
    audio = extract_audio(video_path)

    # 3. Transcribe 
    transcript = transcribe_audio(audio)

    # 4. Caption
    # TODO: Generate captions using the selected backend.

    preprocessed = {
        "frames": [str(frame) for frame in frames],
        "transcript": transcript,
    }
    
    return preprocessed

if __name__ == "__main__":
    video_path = VIDEO_DIR / "examples/e1.mp4" 
    result = run_pipeline(video_path, "gemini")
    print("Result:")
    print(result)
import subprocess
from pathlib import Path
from config.settings import AUDIO_DIR, VIDEO_DIR

def extract_audio(video_path: str | Path) -> Path:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    task_id = Path(video_path).stem
    audio_path = AUDIO_DIR / f"audio_{task_id}.wav"
    subprocess.run([
        "ffmpeg", 
        "-i", str(video_path),           
        "-vn",                      
        "-acodec", "pcm_s16le",     
        "-ar", "16000",             
        "-ac", "1",                 
        str(audio_path)            
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_path

if __name__ == "__main__":
    # example video
    DIR = VIDEO_DIR / "examples"

    example_files = list(DIR.iterdir())

    if not example_files:
        print("No example videos found.")
    else:
        example_video_path = example_files[0]
        audio_path = extract_audio(example_video_path)
        print(f"Extracted audio to: {audio_path}")
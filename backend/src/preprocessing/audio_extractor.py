import subprocess
from pathlib import Path

from config.settings import AUDIO_DIR, VIDEO_DIR
from src.utils.logger import logger

def has_audio(video_path: str | Path) -> bool:
    """Check if a video file has an audio stream."""
    result = subprocess.run(
    [
        "ffprobe", 
        "-i", str(video_path), 
        "-show_streams", 
        "-select_streams", "a", 
        "-loglevel", "error"
    ],
        capture_output=True, 
        text=True
    )
    return bool(result.stdout)


def extract_audio(video_path: str | Path) -> Path | None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    task_id = Path(video_path).stem
    audio_path = AUDIO_DIR / f"audio_{task_id}.wav"
    
    if audio_path.exists():
        logger.info("Audio already extracted: %s", audio_path.name)
        return audio_path
    
    if not has_audio(video_path):
        logger.warning(
            "No audio stream found in %s. Skipping extraction.",
            Path(video_path).name
        )
        return None
    
    logger.info("Extracting audio from %s...", Path(video_path).name)
    try:
        subprocess.run([
            "ffmpeg", 
            "-i", str(video_path),           
            "-vn",                      
            "-acodec", "pcm_s16le",     
            "-ar", "16000",             
            "-ac", "1",                 
            str(audio_path)            
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("Audio extraction completed: %s", audio_path.name)
    except subprocess.CalledProcessError:
        logger.exception("Audio extraction failed for %s", Path(video_path).name)
        raise
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

    # video with no audio
    videos = list(VIDEO_DIR.iterdir())

    if videos:
        video_path = videos[0]
        response = extract_audio(video_path)
        if response is None:
            print("No audio found")
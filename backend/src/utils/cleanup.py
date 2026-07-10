import shutil

from config.settings import AUDIO_DIR, FRAMES_DIR
from src.utils.logger import logger

def cleanup(task_id: str) -> None:
    # Delete audio file
    audio_path = AUDIO_DIR / f"audio_{task_id}.wav"
    if audio_path.exists():
        audio_path.unlink()
        logger.info(f"Deleted audio file: {audio_path.name}")


    # Delete extracted frames directory
    frames_path = FRAMES_DIR / task_id
    if frames_path.exists():
        shutil.rmtree(frames_path)
        logger.info(f"Deleted frames directory: {frames_path.name}")
    
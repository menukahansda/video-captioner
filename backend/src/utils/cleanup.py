import shutil

from config.settings import AUDIO_DIR, FRAMES_DIR, OUTPUTS_DIR, UPLOADS_DIR
from src.utils.logger import logger


def cleanup(task_id: str) -> None:
    # Delete audio file
    audio_path = AUDIO_DIR / f"audio_{task_id}.wav"
    if audio_path.is_file():
        audio_path.unlink()
        logger.info(f"Deleted audio file: {audio_path.name}")

    # Delete extracted frames directory
    frames_path = FRAMES_DIR / task_id
    if frames_path.is_dir():
        shutil.rmtree(frames_path)
        logger.info(f"Deleted frames directory: {frames_path.name}")
    
    
def _clean_dir_contents(directory) -> None:
    """Remove all contents inside a directory while keeping the directory."""
    if not directory.is_dir():
        return

    for item in directory.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        elif item.is_file():
            item.unlink()
    logger.info(f"Cleaned directory contents: {directory.name}")
         
            
def cleanup_storage() -> None:
    """Remove all uploaded and generated data."""
    _clean_dir_contents(OUTPUTS_DIR)
    _clean_dir_contents(UPLOADS_DIR)
    
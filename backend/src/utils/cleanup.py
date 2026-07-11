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
    
    
def _remove_dir(directory) -> None:
    """Remove a directory entirely, including itself."""
    if directory.is_dir():
        shutil.rmtree(directory)
         
            
def cleanup_storage(dir) -> None:
    """Remove all uploaded and generated data."""
    _remove_dir(OUTPUTS_DIR / dir)
    _remove_dir(UPLOADS_DIR / dir)
    logger.info(f"Removed directory: {dir}")
     
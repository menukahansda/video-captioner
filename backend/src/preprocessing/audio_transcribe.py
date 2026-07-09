from faster_whisper import WhisperModel
from pathlib import Path
from config.settings import AUDIO_DIR
from src.utils.logger import logger

logger.info("Loading Faster-Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")
logger.info("Faster-Whisper model loaded.")

def transcribe_audio(audio_path: str | Path) -> str:
    """Transcribe an audio file to text using Faster-Whisper."""
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"{audio_path} does not exist")
    
    logger.info("Transcribing audio: %s", audio_path.name)
    segments, _ = model.transcribe(
        str(audio_path), 
        beam_size=5, 
        vad_filter=True,
    )
    
    result = "".join(seg.text for seg in segments)
    logger.info("Audio transcription completed: %s", audio_path.name)
    return result

# test block
if __name__ == "__main__":
    # example audio
    example_audio_path = AUDIO_DIR / "audio_e1.wav"
    result = transcribe_audio(example_audio_path)
    print("Transcribed result :")
    print(result)
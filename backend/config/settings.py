from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"
VIDEO_DIR=DATA_DIR/"videos"
MAX_KEYFRAMES=12

# Temporary/intermediate processing folders (gitignored)
AUDIO_DIR = DATA_DIR / "audio"
FRAMES_DIR = DATA_DIR / "frames"

# User inputs and generated results (gitignored)
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUTS_DIR = DATA_DIR / "outputs"

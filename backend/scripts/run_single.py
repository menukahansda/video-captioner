import argparse
import json
import sys
from pathlib import Path
import uuid

from config.settings import OUTPUTS_DIR
from src.pipeline import run_pipeline
from src.utils.cleanup import cleanup
from src.utils.logger import logger


def main():
    """Parse CLI arguments and process a single video."""
    parser = argparse.ArgumentParser(description="Video Captioner")

    parser.add_argument("video", help="Path to the input video file")
    parser.add_argument(
        "--backend",
        choices=["gemini", "local"],
        default="gemini"
    )

    args = parser.parse_args()
    video_path = Path(args.video)
    if not video_path.exists():
        logger.error(f"Video not found: {video_path}")
        sys.exit(1)
        
    task_id = f"{video_path.stem}_{uuid.uuid4().hex[:8]}"
    
    try:
        result = run_pipeline(video_path, task_id, args.backend)
    
        if result is None:
            logger.error("Pipeline failed.")
            sys.exit(1)
        
        # save result to output folder
        output_file = OUTPUTS_DIR / f"{task_id}.json"
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        logger.info(f"Results saved to {output_file}")
        
    except Exception:
        logger.exception("Unexpected error")
        sys.exit(1)
        
    finally:
        # cleanup intermediate files
        cleanup(task_id)
        
if __name__ == "__main__":
    main()

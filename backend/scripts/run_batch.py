import argparse
import json
from pathlib import Path
import uuid

from config.settings import OUTPUTS_DIR
from src.pipeline import run_pipeline
from src.utils.cleanup import cleanup
from src.utils.logger import logger


def main():
    """Parse CLI arguments and process multiple videos."""
    parser = argparse.ArgumentParser(description="Video Captioner")

    parser.add_argument("videos", nargs="+", help="Path to the input video files")
    parser.add_argument(
        "--backend",
        choices=["gemini", "local"],
        default="gemini",
        help="Choose the caption generation backend (default: gemini)"
    )

    args = parser.parse_args()
        
    for video in args.videos:
        video_path = Path(video)
        if not video_path.is_file():
            logger.error(f"Video file not found: {video_path}")
            continue
        
        task_id = f"{video_path.stem}_{uuid.uuid4().hex[:8]}"
    
        try:
            result = run_pipeline(video_path, task_id, args.backend)
    
            if result is None:
                logger.error(f"Pipeline failed for {video_path}")
                continue
        
            # save result to output folder
            output_file = OUTPUTS_DIR / f"{task_id}.json"
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)

            logger.info(f"Results saved to {output_file}")
        
        except Exception:
            logger.exception(f"Unexpected error while processing {video_path}")
        
        finally:
            # cleanup intermediate files
            cleanup(task_id)
        logger.info("-" * 40)
        
if __name__ == "__main__":
    main()

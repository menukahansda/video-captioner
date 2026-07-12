import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.preprocessing.downloader import download_video
from src.pipeline import run_pipeline
from src.utils.logger import logger

INPUT_PATH = Path("input/tasks.json")
OUTPUT_PATH = Path("output/results.json")
DEBUG_PATH = Path("debug/summaries.json")
MAX_WORKERS = 4  

def process_task(task):
    task_id = task["task_id"]
    video_url = task["video_url"]
    styles = task["styles"] 

    summary = {}
    captions = {}
    error = None
    try:
        video_path = download_video(video_url, task_id)
        result = run_pipeline(video_path, task_id, styles, "gemini")
        summary = result.get("summary", {})
        captions = result.get("captions", {})
    except Exception as e:
        logger.exception(f"Task {task_id} failed")
        error = str(e)

    return {
        "task_id": task_id, 
        "captions": captions, 
        "_debug": {"summary": summary, "error": error},
    }

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    results = []
    debug_data = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_task = {executor.submit(process_task, task): task for task in tasks}
        for future in as_completed(future_to_task):
            r = future.result()
            debug_data[r["task_id"]] = r.pop("_debug")
            results.append(r)

    # Restore original task order 
    order = {task["task_id"]: i for i, task in enumerate(tasks)}
    results.sort(key=lambda r: order[r["task_id"]])

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    DEBUG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DEBUG_PATH, "w", encoding="utf-8") as f:
        json.dump(debug_data, f, indent=2)
    
    logger.info(f"Wrote {len(results)} results, debug info at {DEBUG_PATH}")

if __name__ == "__main__":
    main()
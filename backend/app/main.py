from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
from pathlib import Path
import uuid

from src.pipeline import run_pipeline
from src.utils.cleanup import cleanup, cleanup_storage
from src.utils.logger import logger
from config.settings import UPLOADS_DIR, OUTPUTS_DIR

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Message"],
)

port = int(os.getenv("PORT", 8000))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/cleanup/{userId}")
def cleanup_task(userId: str):
    cleanup_storage(userId)
    return JSONResponse(content={"message": "Input/Output folder cleared"}, status_code=200)

@app.post("/generate-captions")
async def generate_captions(
    userId: str = Form(...),
    videos: list[UploadFile] = File(...),
):
    if not videos:
        return JSONResponse(status_code=400, content={"error": "No video files uploaded"})
    print("Received video files:", [video.filename for video in videos])
    
    # create folder and add videos
    os.makedirs(UPLOADS_DIR / userId, exist_ok=True)
    os.makedirs(OUTPUTS_DIR / userId, exist_ok=True)
    upload_dir = UPLOADS_DIR / userId
    output_dir = OUTPUTS_DIR / userId
    
    for video in videos:
        safe_stem = Path(video.filename).stem
        suffix = Path(video.filename).suffix or ".mp4" 
        video_path = upload_dir / f"{safe_stem}_{uuid.uuid4().hex[:8]}{suffix}"
        with open(video_path, "wb") as file:
            content = await video.read()
            file.write(content)

    logger.info("Videos files saved to disk.")

    # run the actual pipeline
    results = {}
    for video_path in upload_dir.iterdir():
        try:
            task_id = video_path.stem
            result = run_pipeline(video_path, task_id, "gemini")
    
            if result is None:
                logger.error(f"Pipeline failed for {task_id}.")
                continue
        
            # save result to output folder
            output_file = output_dir / f"{task_id}.json"
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)
            results[task_id] = result
            logger.info(f"Results saved to {output_file}")

        except Exception:
            logger.exception(f"Unexpected error processing {task_id}")
        finally:
            # cleanup intermediate files
            cleanup(task_id)
        logger.info("-" * 40)

    return JSONResponse(
        content={"user": userId, "results": results},
        headers={"X-Message": "Videos processed successfully"},
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
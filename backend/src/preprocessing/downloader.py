import requests
from pathlib import Path
from config.settings import VIDEO_DIR

def download_video(video_url:str,task_id:str)->Path:
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    video_path=VIDEO_DIR/f"{task_id}.mp4"
    response = requests.get(video_url, stream=True, timeout=30)
    response.raise_for_status(); 
    with open(video_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)  
    return video_path

if __name__ == "__main__":
    url="https://storage.googleapis.com/amd-hackathon-clips/1860079-uhd_2560_1440_25fps.mp4"
    saved_path=download_video(url,"v1")
    print(f"Downloaded to:{saved_path}")
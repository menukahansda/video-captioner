import cv2
from pathlib import Path
def validate_video(video_path:Path):
    if not video_path.exists():
        raise FileExistsError(f"Video not found:{video_path}")
    cap=cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Unable to open video:{video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if fps<=0:
        cap.release()
        raise ValueError("Invalide FPS.Cannot calculate video duration.")
    duration=frame_count/fps
    if duration>120:
        cap.release()
        raise ValueError("Video exceeds the maximum allowed duration of 2 minutes.")
    cap.release()

    return {
        "fps":fps,
        "frame_count":frame_count,
        "duration":duration,
        "width":width,
        "height":height
    }

if __name__=="__main__":
    from config.settings import VIDEO_DIR
    video_path=VIDEO_DIR/"v1.mp4"
    metadata=validate_video(video_path)
    print(metadata)
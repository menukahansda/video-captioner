from pathlib import Path
import cv2

#To open and track the video for scene detection and its changes
from scenedetect import open_video,SceneManager
from scenedetect.detectors import ContentDetector

from config.settings import FRAMES_DIR, MAX_KEYFRAMES
from src.utils.logger import logger

MIN_KEYFRAMES = 6         
SECONDS_PER_FRAME = 8

def _compute_target_frame_count(duration_seconds: float) -> int:
    target = int(duration_seconds // SECONDS_PER_FRAME)
    return max(MIN_KEYFRAMES, min(MAX_KEYFRAMES, target))

def extract_keyframes(video_path:Path,task_id:str):
    output_dir=FRAMES_DIR/task_id
    output_dir.mkdir(parents=True,exist_ok=True)

    for file in output_dir.glob("*.jpg"):
        file.unlink()
    
    cap=cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError("Unable to open video.")
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        cap.release()
        raise ValueError("Invalid FPS.")
    
    duration_seconds = total_frames / fps
    target_frame_count = _compute_target_frame_count(duration_seconds)
    
    #Scene Detection
    video=open_video(str(video_path))
    scene_manager=SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=27))
    
    logger.info("Detecting scenes for %s...", video_path.name)
    scene_manager.detect_scenes(video)
    scene_list=scene_manager.get_scene_list()
    # print(f"Number of scenes detected: {len(scene_list)}")
    # print(scene_list)
    
    saved_frames=[]
    frame_numbers_used = set()
    
    interval = max(1, total_frames // target_frame_count)
    for frame_number in range(0, total_frames, interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = cap.read()
        if not success:
            continue
        frame_path = output_dir / f"frame_{len(saved_frames) + 1:03d}.jpg"
        cv2.imwrite(str(frame_path), frame)
        saved_frames.append(frame_path)
        frame_numbers_used.add(frame_number)
        if len(saved_frames) >= MAX_KEYFRAMES:
            break

    if len(scene_list) > 1 and len(saved_frames) < MAX_KEYFRAMES:
        logger.info("%d scenes detected — adding scene-boundary frames.", len(scene_list))
        for start_time, end_time in scene_list:
            middle_frame = (start_time.frame_num + end_time.frame_num) // 2
            if any(abs(middle_frame - f) < interval // 2 for f in frame_numbers_used):
                continue  # close enough to an existing sample, skip
            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
            success, frame = cap.read()
            if not success:
                continue
            frame_path = output_dir / f"frame_{len(saved_frames) + 1:03d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            saved_frames.append(frame_path)
            frame_numbers_used.add(middle_frame)
            if len(saved_frames) >= MAX_KEYFRAMES:
                break
    else:
        logger.info("No significant scene cuts detected — using interval sampling only.")

    cap.release()
    logger.info("Extracted %d keyframes from %s.", len(saved_frames), video_path.name)
    return saved_frames
    
    
# if __name__=="__main__":
#     from config.settings import VIDEO_DIR
#     video=VIDEO_DIR/"v1.mp4"
#     frames=extract_keyframes(video,"v1")
#     print("\nSaved Frames:")
#     for frame in frames:
#         print(frame)
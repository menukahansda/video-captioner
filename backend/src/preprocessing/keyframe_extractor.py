from pathlib import Path
import cv2

#To open and track the video for scene detection and its changes
from scenedetect import open_video,SceneManager
from scenedetect.detectors import ContentDetector

from config.settings import FRAMES_DIR, MAX_KEYFRAMES
from src.utils.logger import logger

def extract_keyframes(video_path:Path,task_id:str):
    output_dir=FRAMES_DIR/task_id
    output_dir.mkdir(parents=True,exist_ok=True)

    for file in output_dir.glob("*.jpg"):
        file.unlink()
    #Scene Detection
    video=open_video(str(video_path))
    scene_manager=SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=8))
    
    logger.info("Detecting scenes for %s...", video_path.name)
    scene_manager.detect_scenes(video)
    scene_list=scene_manager.get_scene_list()
    # print(f"Number of scenes detected: {len(scene_list)}")
    # print(scene_list)
    cap=cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError("Unable to open video.")
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        cap.release()
        raise ValueError("Invalid FPS.")
    
    saved_frames=[]
    if len(scene_list) > 0:
        logger.info("%d scenes detected.", len(scene_list))
        for index,scene in enumerate(scene_list):
            start_time,end_time=scene
            start_frame=start_time.frame_num
            end_frame=end_time.frame_nums
            middle_frame=(start_frame+end_frame)//2
            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
            
            success, frame = cap.read()
            if not success:
                continue
            frame_path=output_dir/f"frame_{index + 1:03d}.jpg"
            cv2.imwrite(str(frame_path),frame)
            saved_frames.append(frame_path)
            if len(saved_frames)>=MAX_KEYFRAMES:
                break
    else:
        logger.warning("No scenes detected. Using interval sampling...")
        desired_frames = min(MAX_KEYFRAMES, 8)
        interval_frames = max(1, total_frames // desired_frames)

        for frame_number in range(0, total_frames, interval_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            success, frame = cap.read()
            if not success:
                continue
            frame_path = output_dir / f"frame_{len(saved_frames)+1:03d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            saved_frames.append(frame_path)
            if len(saved_frames) >= MAX_KEYFRAMES:
                break
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
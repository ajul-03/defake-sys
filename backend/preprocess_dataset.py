
import os
import glob
import numpy as np
import config
import preprocess
from tqdm import tqdm

def get_video_paths():
    """
    Scans the dataset directories and returns lists of real and fake video paths.
    """
    print(f"Scanning for videos...")
    real_videos = glob.glob(os.path.join(config.REAL_VIDEOS_DIR, "**", "*.mp4"), recursive=True) + \
                  glob.glob(os.path.join(config.REAL_VIDEOS_DIR, "**", "*.avi"), recursive=True)
    
    fake_videos = glob.glob(os.path.join(config.FAKE_VIDEOS_DIR_1, "**", "*.mp4"), recursive=True) + \
                  glob.glob(os.path.join(config.FAKE_VIDEOS_DIR_1, "**", "*.avi"), recursive=True)
    
    print(f"Found {len(real_videos)} real videos.")
    print(f"Found {len(fake_videos)} fake videos.")
    
    return real_videos, fake_videos

def process_and_save(video_path, output_dir, label_name, num_clips=1):
    """
    Process a single video and save it as multiple .npy files (clips).
    """
    try:
        # Create a unique filename based on the video name
        video_name = os.path.basename(video_path)
        base_name = os.path.splitext(video_name)[0]
        
        # 1. Extract multiple clips
        # Returns list of numpy arrays, each (frames, h, w, c)
        video_clips = preprocess.extract_multiple_clips(
            video_path, 
            num_clips=num_clips, 
            frames_per_clip=config.FRAME_COUNT
        )
        
        if len(video_clips) == 0:
            return

        for i, raw_frames in enumerate(video_clips):
            # If num_clips > 1, add suffix. If = 1, keep simple name for backward compat if desired, 
            # but cleaner to always suffix if we are doing multi-extract logic generally.
            # Let's use suffix always for clarity: _clip1, _clip2
            clip_suffix = f"_clip{i+1}"
            output_filename = f"{label_name}_{base_name}{clip_suffix}.npy"
            output_path = os.path.join(output_dir, output_filename)
            
            # Skip if already exists
            if os.path.exists(output_path):
                continue

            # 2. Process Faces (Detect -> Crop -> Resize -> Normalize)
            processed_frames = preprocess.detect_and_crop_faces(raw_frames, config.IMG_SIZE)
            
            # 3. Pad if necessary
            if len(processed_frames) < config.FRAME_COUNT:
                padding = np.zeros((config.FRAME_COUNT - len(processed_frames), config.IMG_SIZE[0], config.IMG_SIZE[1], 3))
                processed_frames = np.concatenate([processed_frames, padding], axis=0)
            
            # 4. Save
            # Save without batch dimension: (frames, h, w, c)
            np.save(output_path, processed_frames.astype('float16'))
        
    except Exception as e:
        print(f"Error processing {video_path}: {e}")

def main():
    # 1. Setup Directories
    real_processed_dir = os.path.join(config.PROCESSED_DATA_DIR, "real")
    fake_processed_dir = os.path.join(config.PROCESSED_DATA_DIR, "fake")
    
    os.makedirs(real_processed_dir, exist_ok=True)
    os.makedirs(fake_processed_dir, exist_ok=True)
    
    # 2. Get Paths
    real_paths, fake_paths = get_video_paths()
    
    # 3. Process Real Videos
    print(f"\nProcessing Real Videos ({len(real_paths)} videos)...")
    for path in tqdm(real_paths):
        # We process all real videos with 2 clips per video to maximize data
        process_and_save(path, real_processed_dir, "real", num_clips=2)
        
    # 4. Process Fake Videos
    print(f"\nProcessing Fake Videos ({len(fake_paths)} videos)...")
    for path in tqdm(fake_paths):
        process_and_save(path, fake_processed_dir, "fake", num_clips=2)
        
    print(f"\nPreprocessing Complete!")
    print(f"Processed data saved to: {config.PROCESSED_DATA_DIR}")

if __name__ == "__main__":
    main()

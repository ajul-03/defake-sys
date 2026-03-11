
import os
import config
import preprocess
import numpy as np
import glob

def test_preprocess_one_fake():
    print("Testing preprocessing on one fake video...")
    
    # Get one fake video
    fake_videos = glob.glob(os.path.join(config.FAKE_VIDEOS_DIR_1, "**", "*.mp4"), recursive=True)
    if not fake_videos:
        print("No fake videos found!")
        return
        
    target_video = fake_videos[0]
    print(f"Target: {target_video}")
    
    try:
        data = preprocess.preprocess_video(target_video, max_frames=config.FRAME_COUNT, img_size=config.IMG_SIZE)
        print(f"Result shape: {data.shape}")
        
        if data.shape == (1, config.FRAME_COUNT, *config.IMG_SIZE, 3):
            print("SUCCESS: Preprocessing worked.")
            # Check content (not all zeros)
            if np.max(data) > 0:
                print("Data contains non-zero values.")
            else:
                print("WARNING: Data is all zeros (black frames?).")
        else:
            print("FAILURE: Incorrect shape.")
            
    except Exception as e:
        print(f"FAILURE: Exception occurred: {e}")

if __name__ == "__main__":
    test_preprocess_one_fake()

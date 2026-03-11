import os
import glob
import config

with open("debug_output.txt", "w") as f:
    f.write(f"ROOT_DIR: {config.ROOT_DIR}\n")
    f.write(f"FAKE_VIDEOS_DIR_1: {config.FAKE_VIDEOS_DIR_1}\n")

    if os.path.exists(config.FAKE_VIDEOS_DIR_1):
        f.write("Fake videos directory EXISTS.\n")
        files = os.listdir(config.FAKE_VIDEOS_DIR_1)
        f.write(f"Total files in directory: {len(files)}\n")
    else:
        f.write("Fake videos directory DOES NOT EXIST.\n")

    f.write("Running glob...\n")
    fake_videos = glob.glob(os.path.join(config.FAKE_VIDEOS_DIR_1, "**", "*.mp4"), recursive=True)
    f.write(f"Glob found {len(fake_videos)} .mp4 files.\n")

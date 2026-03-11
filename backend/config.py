
import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

REAL_VIDEOS_DIR = os.path.join(ROOT_DIR, "original")
FAKE_VIDEOS_DIR_1 = os.path.join(ROOT_DIR, "Deepfakes")


# Directory where preprocessed .npy files will be saved
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "dataset_processed")

# --- Model & Training Parameters ---
IMG_SIZE = (299, 299)
FRAME_COUNT = 20
BATCH_SIZE = 2 # Keep small for video data
EPOCHS = 20
LEARNING_RATE = 0.0001
TEST_SPLIT = 0.3
RANDOM_SEED = 42

# --- Model Weights ---
MODEL_WEIGHTS_PATH = os.path.join(BASE_DIR, 'model_weights.h5')
FINAL_MODEL_PATH = os.path.join(BASE_DIR, 'deepfake_model_final.h5')

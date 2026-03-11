import os
import glob
import numpy as np
import config
from train import AugmentedDataGenerator

def test_gen():
    print("Testing Generator...")
    
    # Get a few files
    real_files = sorted(glob.glob(os.path.join(config.PROCESSED_DATA_DIR, "real", "*.npy")))[:4]
    fake_files = sorted(glob.glob(os.path.join(config.PROCESSED_DATA_DIR, "fake", "*.npy")))[:4]
    
    X = real_files + fake_files
    y = [0]*len(real_files) + [1]*len(fake_files)
    
    if len(X) == 0:
        print("No data found! Make sure dataset is preprocessed.")
        return

    gen = AugmentedDataGenerator(X, y, batch_size=2, augment=True)
    
    print(f"Generator length: {len(gen)}")
    
    try:
        batch_X, batch_y = gen[0]
        print(f"Batch X shape: {batch_X.shape}")
        print(f"Batch y shape: {batch_y.shape}")
        print(f"Batch X min/max values: {np.min(batch_X)} / {np.max(batch_X)}")
        assert np.min(batch_X) >= 0.0, "Pixels scaled below 0"
        assert np.max(batch_X) <= 255.0, "Pixels scaled above 255"
        print("Generator test PASSED.")
    except Exception as e:
        print(f"Generator test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gen()

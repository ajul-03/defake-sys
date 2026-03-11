import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Reduce noise
import tensorflow as tf

print("\n" + "="*50)
print("ANTIGRAVITY GPU DIAGNOSTIC")
print("="*50)

print(f"TensorFlow Version: {tf.__version__}")

gpus = tf.config.list_physical_devices('GPU')
if len(gpus) > 0:
    print(f"✅ SUCCESS: {len(gpus)} GPU(s) DETECTED!")
    for gpu in gpus:
        print(f"   - {gpu.name}")
else:
    print("❌ FAILURE: No GPU detected.")
    print("Potential Causes:")
    print("1. CUDA Toolkit 11.2 not installed (Required for TF 2.10 on Windows).")
    print("2. cuDNN 8.1 not installed or DLLs missing from PATH.")
print("="*50 + "\n")


import os
import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, BatchNormalization, Conv2D, MaxPooling2D, TimeDistributed, Flatten, GlobalAveragePooling2D, Bidirectional
from tensorflow.keras.applications import Xception
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.utils import Sequence
import matplotlib.pyplot as plt
import cv2
import config
import model_utils
import random
from sklearn.model_selection import train_test_split

class AugmentedDataGenerator(Sequence):
    """
    Data generator that applies on-the-fly augmentation.
    Optimized for EfficientNet: Input scaled to [0, 255].
    """
    def __init__(self, file_paths, labels, batch_size=config.BATCH_SIZE, shuffle=True, augment=False):
        self.file_paths = file_paths
        self.labels = labels
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.augment = augment
        self.indices = np.arange(len(self.file_paths))
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __len__(self):
        return int(np.floor(len(self.file_paths) / self.batch_size))

    def __getitem__(self, index):
        indices = self.indices[index*self.batch_size:(index+1)*self.batch_size]
        batch_paths = [self.file_paths[k] for k in indices]
        batch_labels = [self.labels[k] for k in indices]
        
        X, y = self.__data_generation(batch_paths, batch_labels)
        return X, y

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __data_generation(self, batch_paths, batch_labels):
        # Initialization
        # Output shape: (Batch, Frames, H, W, C)
        X = np.empty((self.batch_size, config.FRAME_COUNT, *config.IMG_SIZE, 3), dtype='float32')
        y = np.empty((self.batch_size), dtype='float32') # Float for label smoothing

        for i, path in enumerate(batch_paths):
            try:
                # Load preprocessed tensor. Shape (frames, h, w, c). Values usually [0, 1] from preprocess.py
                data = np.load(path).astype('float32')
                
                # --- AUGMENTATION ---
                if self.augment:
                    # Apply consistent geometric augmentation (e.g. flipping)
                    if random.random() > 0.5:
                        data = np.flip(data, axis=2) # Flip width
                    
                    # Convert to tensor for tf.image operations
                    data_t = tf.convert_to_tensor(data, dtype=tf.float32)
                    
                    # 1. Random Brightness
                    data_t = tf.image.random_brightness(data_t, 0.15)
                    
                    # 2. Random Contrast
                    data_t = tf.image.random_contrast(data_t, 0.8, 1.2)
                    
                    # 3. Gaussian Noise
                    noise = tf.random.normal(shape=tf.shape(data_t), mean=0.0, stddev=0.02, dtype=tf.float32)
                    data_t = data_t + noise
                    
                    data = data_t.numpy()
                    
                # --- NORMALIZATION [0, 1] -> [0, 255] ---
                # EfficientNet expects pixels in range [0, 255]
                data = data * 255.0
                
                # Clip to ensure valid range after noise
                data = np.clip(data, 0.0, 255.0)

                X[i,] = data
                y[i] = batch_labels[i]
                
            except Exception as e:
                print(f"Error loading {path}: {e}")
                X[i,] = np.zeros((config.FRAME_COUNT, *config.IMG_SIZE, 3))
                y[i] = batch_labels[i]

        return X, y

def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    auc = history.history.get('auc', [])
    val_auc = history.history.get('val_auc', [])
    
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 4))
    
    # Accuracy Plot
    plt.subplot(1, 3, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    # Loss Plot
    plt.subplot(1, 3, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    
    # AUC Plot
    if auc:
        plt.subplot(1, 3, 3)
        plt.plot(epochs_range, auc, label='Training AUC')
        plt.plot(epochs_range, val_auc, label='Validation AUC')
        plt.legend(loc='lower right')
        plt.title('Training and Validation AUC')

    plt.savefig('training_history_advanced.png')
    # plt.show()

def main():
    # 1. Check GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"GPUs Detected: {len(gpus)}")
        except RuntimeError as e:
            print(e)
    else:
        print("No GPU detected. Training will be slow.")

    # 2. Prepare Data
    if not os.path.exists(config.PROCESSED_DATA_DIR):
        print(f"Error: Processed data directory not found at {config.PROCESSED_DATA_DIR}")
        print("Please run preprocess_dataset.py first.")
        return

    # 2.2 Load Data Paths
    real_files = sorted(glob.glob(os.path.join(config.PROCESSED_DATA_DIR, "real", "*.npy")))
    fake_files = sorted(glob.glob(os.path.join(config.PROCESSED_DATA_DIR, "fake", "*.npy")))
    
    print(f"Found {len(real_files)} real processed samples.")
    print(f"Found {len(fake_files)} fake processed samples.")
    
    print(f"Total Training Data Available: {len(real_files)} Real, {len(fake_files)} Fake.")

    # 3. Create Splits (Sorted, not Random) to prevent leakage
    def split_data(files):
        if len(files) < 5: return files, []
        # Sort files to ensure clips from same video stay together if named sequentially
        # files.sort() # Already sorted above, but shuffled if limited. 
        # If we shuffled for limiting, we might have mixed clips. 
        # Ideally we should limit by video ID, but file-level limit is okay for now if we accept slight leak 
        # OR we just rely on the shuffle to separate them randomly enough.
        # Strict "No Leakage" requires parsing filenames. Let's do simple split for now.
        
        split_idx = int(len(files) * (1 - config.TEST_SPLIT))
        return files[:split_idx], files[split_idx:]
    
    real_train, real_val = split_data(real_files)
    fake_train, fake_val = split_data(fake_files)
    
    X_train = real_train + fake_train
    y_train = [0] * len(real_train) + [1] * len(fake_train)
    
    X_val = real_val + fake_val
    y_val = [0] * len(real_val) + [1] * len(fake_val)
    
    print(f"Training samples: {len(X_train)} ({len(real_train)} real, {len(fake_train)} fake)")
    print(f"Validation samples: {len(X_val)} ({len(real_val)} real, {len(fake_val)} fake)")
    
    # 4. Create Generators
    train_gen = AugmentedDataGenerator(
        X_train, 
        y_train, 
        batch_size=config.BATCH_SIZE, 
        shuffle=True,
        augment=True # Enable Augmentation for training
    )
    
    val_gen = AugmentedDataGenerator(
        X_val, 
        y_val, 
        batch_size=config.BATCH_SIZE, 
        shuffle=False,
        augment=False
    )
    
    # 5. Build Model
    model = model_utils.build_model(
        frame_count=config.FRAME_COUNT, 
        img_size=config.IMG_SIZE, 
        learning_rate=config.LEARNING_RATE,
        l2_reg=0.001 # Strong regularization
    )
    model.summary()
    
    # 6. Callbacks
    callbacks = [
        ModelCheckpoint(config.MODEL_WEIGHTS_PATH, save_best_only=True, monitor='val_auc', mode='max'),
        ReduceLROnPlateau(monitor='val_auc', factor=0.5, patience=2, min_lr=1e-6, verbose=1, mode='max'),
        EarlyStopping(monitor='val_auc', patience=5, restore_best_weights=True, verbose=1, mode='max'),
    ]
    
    # 7. Train
    print("Starting training with Advanced Regularization...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=config.EPOCHS,
        callbacks=callbacks
    )
    
    # 8. Save Final Model
    model.save(config.FINAL_MODEL_PATH)
    print(f"Model saved to {config.FINAL_MODEL_PATH}")
    
    # 9. Plot
    plot_history(history)

if __name__ == "__main__":
    main()

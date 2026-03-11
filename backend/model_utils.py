import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import LSTM, Dense, Dropout, TimeDistributed, GlobalAveragePooling2D, Input, Bidirectional, SpatialDropout1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
import preprocess
import os

# --- GPU Configuration ---
# Optional: Set memory growth to prevent TF from hogging all VRAM
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

def build_model(frame_count=20, img_size=(299, 299), learning_rate=0.0001, l2_reg=0.001):
    """
    Builds and compiles the Deepfake Detection Model.
    
    Architecture:
    1. Input: Sequence of frames (Batch, Frames, Height, Width, Channels)
    2. TimeDistributed Xception: Extracts spatial features from EACH frame independently.
    3. Bidirectional LSTM: Analyzes the temporal sequence of features (change over time).
    4. Attention Layer: Focuses on the most relevant frames in the sequence.
    5. Classifier: Dense layers to output a probability (Real vs Fake).
    
    Args:
        frame_count (int): Number of frames per video sequence.
        img_size (tuple): Height and width of frames.
        learning_rate (float): Learning rate for the optimizer.
        l2_reg (float): L2 Regularization factor.
        
    Returns:
        model: A compiled TensorFlow Keras model.
    """
    
    # 1. CNN Base: EfficientNetB0 (Feature Extractor)
    # EfficientNet is generally faster and better than Xception
    from tensorflow.keras.applications import EfficientNetB0
    cnn_base = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(img_size[0], img_size[1], 3))
    
    # Freeze the CNN initially so we don't destroy pre-trained ImageNet weights during initial training
    # For "more than good", we might want to unfreeze top layers later, but keep strict frozen for now
    cnn_base.trainable = False 
    
    cnn_out = GlobalAveragePooling2D()(cnn_base.output)
    cnn_model = Model(inputs=cnn_base.input, outputs=cnn_out)

    # 2. Sequence Input
    video_input = Input(shape=(frame_count, img_size[0], img_size[1], 3))
    
    # 3. Distribute CNN across time (apply to every frame)
    # This turns (Batch, Frames, H, W, C) -> (Batch, Frames, Feature_Vector)
    encoded_frames = TimeDistributed(cnn_model)(video_input)
    
    # NEW: Spatial Dropout drops entire feature maps/channels across the sequence
    # This is better for temporal data than standard Dropout, forcing the model to not rely on specific features
    x = SpatialDropout1D(0.3)(encoded_frames)
    
    # 4. Temporal Analysis
    # Bidirectional LSTM sees the sequence forward and backward to catch anomalies
    # Add L2 Regularization to prevent weights from exploding
    # Reduced units to 128 to combat overfitting
    x = Bidirectional(LSTM(128, return_sequences=True, kernel_regularizer=l2(l2_reg)))(x) 
    
    # 5. Attention Mechanism
    # Helps the model focus on frames where the partial deepfake is most visible
    x = AttentionLayer()(x) 
    
    x = Dropout(0.6)(x) # Prevent overfitting (increased from 0.5)
    
    # Dense Layer with L2 Regularization
    # Reduced units to 64 to combat overfitting
    x = Dense(64, activation='relu', kernel_regularizer=l2(l2_reg))(x)
    x = Dropout(0.6)(x)
    
    outputs = Dense(1, activation='sigmoid')(x) # 0 = Real, 1 = Fake (or vice versa depending on labels)
    
    model = Model(inputs=video_input, outputs=outputs)
    
    # Compile the model
    # NEW: AUC Metric is better for imbalance.
    optimizer = Adam(learning_rate=learning_rate)
    
    # Use binary_crossentropy. Note: we will add label smoothing in the training loop or loss function if supported
    # TF 2.x supports label_smoothing in BinaryCrossentropy loss class
    # Increased label smoothing to 0.2
    loss_fn = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.2)
    
    model.compile(loss=loss_fn, optimizer=optimizer, metrics=['accuracy', tf.keras.metrics.AUC(name='auc')])
    
    return model

class AttentionLayer(tf.keras.layers.Layer):
    """
    Custom Attention Layer to weight the importance of different frames.
    """
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='attention_weight',
                                 shape=(input_shape[-1], 1),
                                 initializer='random_normal',
                                 trainable=True)
        self.b = self.add_weight(name='attention_bias',
                                 shape=(input_shape[1], 1),
                                 initializer='zeros',
                                 trainable=True)
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        # x shape: (batch_size, time_steps, features)
        # e = unnormalized attention scores
        e = tf.keras.backend.tanh(tf.keras.backend.dot(x, self.W) + self.b)
        # a = attention weights (softmax ensures they sum to 1)
        a = tf.keras.backend.softmax(e, axis=1)
        # output = weighted sum of input features
        output = x * a
        return tf.keras.backend.sum(output, axis=1)

def load_trained_model(weights_path='model_weights.h5'):
    """
    Builds the model structure and loads saved weights.
    """
    print("Building model architecture...")
    model = build_model()
    
    if os.path.exists(weights_path):
        try:
            print(f"Loading weights from {weights_path}...")
            model.load_weights(weights_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading weights: {e}")
            print("Using initialized random weights (Warning: Predictions will be random).")
    else:
        print(f"Weights file {weights_path} not found. Using random weights.")
        
    return model

def predict_video(model, video_path):
    """
    Predicts if a video is REAL or FAKE using the loaded model.
    """
    print(f"Processing video: {video_path}")
    
    try:
        # 1. Preprocess
        # Returns shape (1, frames, 299, 299, 3) with values [0, 1]
        video_tensor = preprocess.preprocess_video(video_path)
        
        # EfficientNet expects [0, 255], so we rescale
        video_tensor = video_tensor * 255.0
        
        # 2. Predict
        prediction = model.predict(video_tensor)
        
        # 3. Interpret
        confidence = prediction[0][0]
        
        # Assuming 1 = Fake, 0 = Real (standard for binary crossentropy if data is labeled that way)
        # Adjust threshold if needed, usually 0.5
        is_fake = confidence > 0.5
        label = "FAKE" if is_fake else "REAL"
        
        # Normalize confidence to percentage 0-100% relative to the label
        display_confidence = confidence if is_fake else (1 - confidence)
        
        return {
            "result": label,
            "confidence": float(display_confidence),
            "raw_score": float(confidence)
        }
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"result": "ERROR", "confidence": 0.0, "raw_score": 0.0}

import os


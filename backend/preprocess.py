import cv2
import numpy as np
import os
try:
    from mtcnn import MTCNN
    # We still import MTCNN to avoid breaking existing imports, but we won't use it by default now
    MTCNN_AVAILABLE = True
except ImportError:
    print("Warning: MTCNN not installed.")
    MTCNN_AVAILABLE = False

# Load Haar Cascade (standard OpenCV model for frontal face)
HAAR_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

def extract_frames(video_path, max_frames=20):
    """
    Extracts a fixed number of frames from a video.
    Legacy function kept for compatibility.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames <= 0:
        return []
    
    # Calculate interval to get evenly spaced frames
    interval = max(1, total_frames // max_frames)
    
    count = 0
    
    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        if count % interval == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            
        count += 1
        
    cap.release()
    return frames

def extract_multiple_clips(video_path, num_clips=1, frames_per_clip=20):
    """
    Extracts multiple distinct 20-frame clips from a single video.
    Returns a list of frame lists: [[frame1...frame20], [frame1...frame20]]
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames <= 0:
        return []
        
    all_clips = []
    
    # Strategy: Divide video into 'num_clips' segments and take frames from each.
    # If video is too short, we might get overlapping or duplicate frames, that is fine for augmentation.
    segment_length = max(total_frames // num_clips, frames_per_clip)
    
    for i in range(num_clips):
        start_frame = i * segment_length
        end_frame = min(start_frame + segment_length, total_frames)
        
        # Ensure we don't go out of bounds
        if start_frame >= total_frames:
            break
            
        current_clip_frames = []
        
        # Calculate interval for this segment
        # We need exactly frames_per_clip frames from this segment
        segment_duration = end_frame - start_frame
        interval = max(1, segment_duration // frames_per_clip)
        
        frame_idx = start_frame
        count = 0
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        while count < frames_per_clip and frame_idx < end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Read frame relative to the clip start
            if (frame_idx - start_frame) % interval == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                current_clip_frames.append(frame)
                count += 1
                
            frame_idx += 1
            
        if len(current_clip_frames) > 0:
            all_clips.append(current_clip_frames)
            
    cap.release()
    return all_clips

def detect_and_crop_faces(frames, img_size=(299, 299)):
    """
    Detects faces in frames using Haar Cascade (FASTER) and crops them. 
    OPTIMIZED: Uses OpenCV Haar Cascade for ~10x speedup over MTCNN.
    Returns: Batch of preprocessed frames ready for the model.
    """
    processed_frames = []
    
    # Keep track of the last known face box to reuse
    last_box = None
    
    for i, frame in enumerate(frames):
        cropped_face = frame
        
        # Detect on first frame, and then every 4th frame (0, 4, 8, 12...)
        should_detect = (i % 4 == 0) or (last_box is None)
        
        if should_detect:
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                # scaleFactor=1.1, minNeighbors=5 are standard
                faces = face_cascade.detectMultiScale(gray, 1.1, 5)
                
                if len(faces) > 0:
                    # Get the largest face: max area = w*h
                    # formatting: (x, y, w, h)
                    best_face = max(faces, key=lambda rect: rect[2] * rect[3])
                    last_box = best_face
            except Exception as e:
                # If detection fails, keep last_box or use none
                pass
                
        # If we have a box (new or cached), crop
        # Note: 'last_box' is separate from 'faces' loop variable
        if last_box is not None:
            x, y, w, h = last_box
            
            # Add some margin
            margin = 0.1
            x_margin = int(w * margin)
            y_margin = int(h * margin)
            
            x1 = max(0, x - x_margin)
            y1 = max(0, y - y_margin)
            x2 = min(frame.shape[1], x + w + x_margin)
            y2 = min(frame.shape[0], y + h + y_margin)
            
            # Sanity check
            if x2 > x1 and y2 > y1:
                cropped_face = frame[y1:y2, x1:x2]

        # Resize to model input size
        try:
            cropped_face = cv2.resize(cropped_face, img_size)
        except Exception:
            # Fallback if crop was invalid
            cropped_face = cv2.resize(frame, img_size)
        
        # Normalize pixel values
        cropped_face = cropped_face / 255.0 
        processed_frames.append(cropped_face)
    
    # Pad with zeros if less than max_frames
    return np.array(processed_frames)

def preprocess_video(video_path, max_frames=20, img_size=(299, 299)):
    """
    Full pipeline: load video -> extract frames -> crop faces -> normalize
    NOTE: This legacy function extracts ONE clip (the first one) to maintain backward compatibility.
    Use extract_multiple_clips for augmentation.
    """
    # Use new logic but just take 1 clip
    clips = extract_multiple_clips(video_path, num_clips=1, frames_per_clip=max_frames)
    
    if len(clips) == 0:
        return np.zeros((1, max_frames, img_size[0], img_size[1], 3))
    
    raw_frames = clips[0]
    processed_frames = detect_and_crop_faces(raw_frames, img_size)
    
    # Pad if necessary
    if len(processed_frames) < max_frames:
        padding = np.zeros((max_frames - len(processed_frames), img_size[0], img_size[1], 3))
        processed_frames = np.concatenate([processed_frames, padding], axis=0)
        
    return np.expand_dims(processed_frames, axis=0) # Add batch dimension: (1, frames, h, w, c)

# Deepfake Video Detection System
## Project Presentation

---

### Slide 1: Welcome
**Project Title**: Deepfake Video Detection System  
**Objective**: To develop a robust, end-to-end system capable of identifying whether a given video is a genuine recording or an artificially manipulated "deepfake" using Deep Learning techniques.

---

### Slide 2: Project Overview
* **Objective**: Automate the process of fake video detection using state-of-the-art Neural Networks.
* **Scope**: The project covers data preprocessing, model training, a backend backend for serving predictions, and a modern frontend interface for user interaction.
* **Outcome**: A web application where users can upload videos and receive an instant classification of REAL or FAKE along with a confidence score.

---

### Slide 3: Problem Statement
* With the rapid advancement of Generative AI, creating hyper-realistic fake videos (deepfakes) has become easily accessible.
* Deepfakes can be used maliciously for misinformation, identity theft, political manipulation, and financial fraud.
* Human eyes can no longer reliably distinguish between authentic and manipulated media.
* There is a critical need for an automated, highly accurate tool to analyze and detect these manipulated temporal and spatial artifacts in videos.

---

### Slide 4: Why This Project is Needed
* **Security & Trust**: To restore trust in digital media by providing a reliable verification mechanism.
* **Scalability**: Manual verification is impossible at the scale of modern social media; automated deep learning models can process videos in seconds.
* **Protection**: To protect individuals and public figures from digital impersonation.
* **Accessibility**: Providing a clear, user-friendly interface allows non-technical users to verify video authenticity easily.

---

### Slide 5: Frontend Explanation
**Technologies Used**:
* **React 19 (via Vite)**: For building the user interface.
* **Tailwind CSS**: For utility-first, modern, and responsive styling.
* **Framer Motion**: For smooth and dynamic animations.
* **React Dropzone**: For handling drag-and-drop video uploads effortlessly.
* **Axios**: For making HTTP requests to the backend API.
* **Lucide React**: For scalable and beautiful icons.

---

### Slide 6: Why Those Frontend Technologies Were Chosen
* **React & Vite**: Fast development server (Vite) and component-based architecture (React) allow for a highly interactive and modular UI.
* **Tailwind CSS**: Rapid UI development. It allows for a premium aesthetic (dark modes, gradients, glassmorphism) without leaving the HTML.
* **Framer Motion**: Adds a premium feel with micro-animations that make the application feel responsive and alive.
* **Axios**: Simplifies handling async API requests and file uploads (FormData).

---

### Slide 7: How the Frontend Works
* The application loads a single-page interface with a futuristic, dark-themed aesthetic.
* The main component is an upload zone (powered by React Dropzone) that accepts `.mp4` and `.avi` files.
* Once a file is dropped, the frontend displays file metadata (name, size) and a "processing" state with animations to keep the user engaged.
* It sends the file via an `Axios` POST request using `FormData` to the backend `/predict` endpoint.
* Upon receiving the response, it transitions to a Results view, displaying "REAL" or "FAKE" and a graphical confidence meter.

---

### Slide 8: User Interface Flow
1. **Landing / Upload**: User opens the app. A sleek drag-and-drop zone prompts the user to upload a video.
2. **File Selection**: User drops a video file. The UI validates the file and shows its details.
3. **Processing**: User clicks "Analyze Video". The UI shows a loading state with spinner and Framer Motion effects.
4. **Backend API Call**: Video is sent. The user waits while the ML model runs inference.
5. **Result Display**: The system gracefully reveals the prediction (Real/Fake) along with a percentage confidence bar.
6. **Reset**: User can click "Upload Another Video" to test again.

---

### Slide 9: Backend Detailed Explanation Overview
The backend is built in Python and is responsible for two major pipelines:
1. **Model Training Pipeline**: Scripts to preprocess data, extract faces, and train the deep learning model.
2. **Inference / API Pipeline**: A Flask server that loads the trained model, receives user videos, processes them, and returns predictions.

*Next, we will break down the specific files used in the backend and why they are necessary.*

---

### Slide 10: Backend File - `app.py`
**Purpose**: The main entry point for the Flask web server.
**How it works**:
* Initializes a Flask app and configures Cross-Origin Resource Sharing (CORS) to allow frontend access.
* Ensures an `uploads/` folder exists for temporary video storage.
* Defines a `/predict` POST route that receives the video from the frontend, saves it, and calls `model_utils.predict_video()`.
* Returns the prediction result (Real/Fake, Confidence) as a JSON response.
**Why it is necessary**: Acts as the bridge between the user's web browser (frontend) and the heavy deep learning inference code.

---

### Slide 11: Backend File - `config.py`
**Purpose**: Centralizes all configuration variables, paths, and hyperparameters.
**How it works**:
* Defines absolute directory paths for the real dataset, fake dataset, and processed `.npy` data.
* Sets critical model hyperparameters: `IMG_SIZE = (299, 299)`, `FRAME_COUNT = 20`, `BATCH_SIZE = 2`, `EPOCHS`, and `LEARNING_RATE`.
* Defines paths for saving the `model_weights.h5`.
**Why it is necessary**: Keeps the codebase clean. If we want to change the image size or batch size, we only modify `config.py` instead of hunting through multiple scripts.

---

### Slide 12: Backend File - `debug_files.py` & `debug_mtcnn.py`
**Purpose**: Troubleshooting and environment validation scripts.
**How it works**:
* `debug_files.py` (formerly referred to as `debug_fill.py`): Checks if the fake video directories exist and counts the `.mp4` files using glob, writing the output to `debug_output.txt`.
* `debug_mtcnn.py`: Attempts to import the MTCNN library and initialize the face detector to ensure the environment is set up correctly.
**Why it is necessary**: Crucial for debugging paths and dependency issues on new environments (like GPU machines) before running long training scripts.

---

### Slide 13: Backend File - `model_utils.py`
**Purpose**: Contains the core Deep Learning architecture and inference logic.
**How it works**:
* `build_model()`: Constructs the complex model using EfficientNetB0 (transfer learning), distributed over time, followed by Spatial Dropout, a Bidirectional LSTM, and a Custom Attention Layer.
* `predict_video()`: Takes a raw video path, calls the preprocessing functions, runs the tensor through the loaded model, and calculates the final confidence score.
**Why it is necessary**: It houses the actual "brain" of the project. Without this file, the neural network structure wouldn't exist, and the web app couldn't make predictions.

---

### Slide 14: Backend File - `preprocess.py`
**Purpose**: Real-time video processing and face extraction.
**How it works**:
* `extract_multiple_clips()`: Divides a video into multiple segments and extracts a uniform number of frames (e.g., 20 frames per clip).
* `detect_and_crop_faces()`: Scans the extracted frames, uses OpenCV's Haar Cascades to find the largest face, crops it with a margin, and resizes it to 299x299. It normalizes pixel values to [0, 1].
**Why it is necessary**: Neural networks need consistent, formatted data. This script ensures every video fed to the model is just a sequence of 20 aligned, cropped faces.

---

### Slide 15: Backend File - `preprocess_dataset.py`
**Purpose**: Offline data preparation for training.
**How it works**:
* Scans the massive dataset of REAL and FAKE videos defined in `config.py`.
* Uses `preprocess.py` to extract multiple facial clips from every video.
* Saves these preprocessed 4D NumPy arrays (frames, height, width, channels) to the disk as `.npy` files.
**Why it is necessary**: Preprocessing videos during training is extremely slow. By doing it once offline and saving `.npy` files, the training process becomes vastly faster and more efficient.

---

### Slide 16: Backend File - `train.py`
**Purpose**: The main training loop to teach the model how to detect deepfakes.
**How it works**:
* Loads paths to all preprocessed `.npy` files and splits them into training and validation sets.
* Uses an `AugmentedDataGenerator` to load batches into memory dynamically, applying data augmentation (flipping, brightness, noise).
* Compiles the model using advanced callbacks (Early Stopping, Learning Rate Reduction, Checkpointing).
* Trains for the specified epochs and plots accuracy/loss graphs.
**Why it is necessary**: This is where the machine learning actually happens. It generates the `model_weights.h5` file that `app.py` uses for future predictions.

---

### Slide 17: Backend File - `test_generator.py`
**Purpose**: Validates the custom Data Generator.
**How it works**:
* Instantiates the `VideoDataGenerator` (from `train.py`) using a tiny subset of the preprocessed data.
* Attempts to fetch a single batch of data (`batch_X, batch_y`) and prints the shapes (e.g., `(2, 20, 299, 299, 3)`).
**Why it is necessary**: Data generators are notoriously tricky to build correctly. This small script allows developers to verify that the batch generation works before committing to a 10-hour training run.

---

### Slide 18: Technologies Used (Backend & AI)
* **Python**: The core programming language for the backend.
* **Flask**: A lightweight, fast web framework to create the API.
* **TensorFlow / Keras**: The Deep Learning framework used to build and train the neural networks.
* **OpenCV (cv2)**: A computer vision library used for reading video frames and detecting faces (via Haar Cascades).
* **NumPy**: Used for heavy array manipulations and saving tensors.

---

### Slide 19: Deep Learning Architecture Selection
* **EfficientNetB0 (Base)**: Chosen over Xception because it provides a better trade-off between accuracy and computational efficiency. It acts as our spatial feature extractor.
* **TimeDistributed Layer**: Allows the EfficientNet model to process each of the 20 frames independently but using the same weights.
* **Bidirectional LSTM**: Analyzes the temporal sequence of features. "Bidirectional" means it looks at the sequence of frames forwards and backwards to catch subtle unnatural movements over time.
* **Custom Attention Layer**: Helps the model focus more weight on specific frames where the deepfake artifacts are most prominent.

---

### Slide 20: Project Working Flow (Input to Output)
1. **User Input**: User uploads a video via the React frontend.
2. **Transmission**: Video is sent over HTTP to the Flask `/predict` endpoint.
3. **Storage**: The backend temporarily saves the video to the `uploads/` folder.
4. **Frame Extraction**: `preprocess.py` opens the video and extracts 20 distinct frames.
5. **Face Detection**: OpenCV finds the face in the frames, crops it, resizes it to 299x299, and normalizes the colors.
6. **Inference**: The sequence of 20 faces is passed into the pre-trained EfficientNet + LSTM model.
7. **Scoring**: The model outputs a probability score between 0.0 and 1.0.
8. **Output**: The API returns JSON. The frontend displays "REAL" or "FAKE" based on the threshold (e.g., > 0.5 is fake).

---

### Slide 21: Results Achieved
* **Output**: The system successfully provides a binary classification (Real/Fake) alongside a specific Confidence Percentage (e.g., 94.5% Confident).
* **Speed**: Thanks to OpenCV Haar Cascades and the efficient EfficientNet architecture, processing a 5-second video clip takes only a few seconds on a modern CPU, and even less on a GPU.
***(Note for user: You can add specific accuracy % from your `training_history.png` graph here)**.

---

### Slide 22: Visual Output
*(Placeholder for Screenshots)*
* Include a screenshot of the beautiful Dark-Themed Frontend UI.
* Include a screenshot of the "Processing" animation state.
* Include a screenshot of the Final Result (Real/Fake confidence bar).
* Include the `training_history.png` graphs showing the AUC, Loss, and Accuracy over epochs.

---

### Slide 23: Challenges Faced
* **Data Scarcity & Imbalance**: Finding high-quality, diverse, and balanced datasets of Real vs. Fake videos.
* **Memory Constraints**: Video data is massive. Loading 20 frames per video for hundreds of videos rapidly exhausted system RAM/VRAM.
* **Slow Preprocessing**: Initially, face detection using MTCNN was aggressively slow, taking minutes per video.
* **Overfitting**: The model rapidly learned the training data but struggled to generalize on the validation set, creating a massive gap in accuracy.

---

### Slide 24: Solutions Implemented
* **Offline Processing (`preprocess_dataset.py`)**: Moved all face detection offline to save Preprocessed `.npy` files, solving RAM bottlenecks during training.
* **OpenCV Haar Cascades**: Replaced MTCNN with OpenCV Haar Cascades in `preprocess.py`, achieving a roughly 10x speedup in face detection.
* **Advanced Regularization**: Introduced `SpatialDropout1D`, strict `L2` regularization in the Dense layers, and Label Smoothing (`0.2`) to combat overfitting.
* **EfficientNet**: Researched and swapped the base model from Xception to EfficientNetB0 for better extraction.

---

### Slide 25: Conclusion
* The Deepfake Video Detection System successfully demonstrates how combining Computer Vision (face extraction) with deep sequential models (LSTMs) can effectively identify manipulated media.
* The separation of concerns (a modular React frontend and a Python Flask backend) ensures the system is resilient, scalable, and easy to maintain.
* The premium UI makes the complex AI approachable for end-users.

---

### Slide 26: Future Scope
* **Audio Analysis**: Many deepfakes also clone voices. Future versions could include an audio spectrogram analysis model (e.g., using Wav2Vec) running in parallel.
* **Cloud Deployment**: Hosting the model on AWS SageMaker or Google Cloud Run for infinite scalability.
* **Real-time Stream Analysis**: Optimizing the pipeline to detect deepfakes during a live video call (e.g., WebRTC, Zoom plugin).
* **Transformer Architectures**: Upgrading the LSTM to a Video Vision Transformer (ViViT) for even higher accuracy.

---

### Slide 27: Thank You / Q&A
* "Thank you for your time."
* "Are there any questions regarding the architecture, the training process, or the frontend implementation?"

---

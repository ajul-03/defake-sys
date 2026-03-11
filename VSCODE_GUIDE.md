# VS Code GPU Setup Guide

This guide ensures you can train your Deepfake model using your GPU in VS Code.

## 1. One-Time Setup
We need to create a special environment with **TensorFlow 2.10**, the last version to support Windows GPUs natively.

1.  Navigate to the `backend` folder in your file explorer.
2.  Double-click **`setup_gpu_env.bat`**.
3.  Wait for it to finish. It will install all required libraries.
    *   *If it fails saying "Python 3.10 not found", please install Python 3.10 from valid source.*

## 2. Training in VS Code (Jupyter)
1.  Open this project in VS Code.
2.  Open **`backend/Deepfake_Detection.ipynb`**.
3.  **Select Kernel** (Top Right):
    *   Click "Select Kernel" -> "Python Environments".
    *   Look for **"Python 3.10 (GPU - Defake)"** or select the `venv_gpu` environment.
4.  Click **Run All**.

## 3. Running the Backend Server
To run the Flask API for the website:

1.  Open a Terminal in VS Code (`Ctrl + ~`).
2.  Run these commands:
    ```powershell
    cd backend
    .\venv_gpu\Scripts\activate
    python app.py
    ```

## Troubleshooting
-   **"No GPU detected"**:
    -   Ensure you have **CUDA Toolkit 11.2** and **cuDNN 8.1** installed on your Windows machine.
    -   Run `backend/check_gpu.py` to diagnose.
-   **Out of Memory (OOM)**:
    -   We enabled Mixed Precision in `train.py`.
    -   If it still crashes, reduce `BATCH_SIZE` in the code from `4` to `2`.

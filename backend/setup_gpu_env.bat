@echo off
setlocal
cd /d "%~dp0"

echo ========================================================
echo   Deepfake Project - GPU Environment Setup (Windows)
echo ========================================================
echo.

:: 1. Check for Python 3.10
echo [1/4] Checking for Python 3.10...
py -3.10 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.10 is not installed or not found via 'py' launcher.
    echo Please install Python 3.10 from python.org or the Microsoft Store.
    echo.
    pause
    exit /b 1
)
echo Found Python 3.10.
echo.

:: 2. Create Virtual Environment
echo [2/4] Creating virtual environment 'venv_gpu'...
if exist venv_gpu (
    echo 'venv_gpu' already exists. Updating it...
) else (
    py -3.10 -m venv venv_gpu
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Created 'venv_gpu'.
)
echo.

:: 3. Install Dependencies
echo [3/4] Installing TensorFlow 2.10 (GPU) and dependencies...
echo This may take a few minutes. Please wait...
echo.

call venv_gpu\Scripts\activate
python -m pip install --upgrade pip
python -m pip install "tensorflow==2.10.1" "protobuf==3.19.6" "numpy<1.24"
python -m pip install mtcnn flask flask-cors opencv-python-headless pandas pillow matplotlib scikit-learn jupyter ipykernel

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo.

:: 4. Register Kernel
echo [4/4] Registering Jupyter Kernel...
python -m ipykernel install --user --name=defake_gpu --display-name "Python 3.10 (GPU - Defake)"

echo.
echo ========================================================
echo   SETUP COMPLETE!
echo ========================================================
echo.
echo You can now open VS Code.
echo In your Jupyter Notebook, select config kernel: "Python 3.10 (GPU - Defake)"
echo.
pause

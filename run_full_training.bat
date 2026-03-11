@echo off
if exist "backend\venv_gpu\Scripts\activate.bat" (
    call "backend\venv_gpu\Scripts\activate.bat"
    echo Activated venv_gpu
) else if exist "backend\venv\Scripts\activate.bat" (
    call "backend\venv\Scripts\activate.bat"
    echo Activated venv
) else (
    echo No virtual environment found. Using system Python.
)
pip install mtcnn
echo Deleting old processed dataset...
rmdir /s /q "backend/dataset_processed"
echo Old dataset deleted.

echo Running Preprocessing (creating new dataset without Face2Face)...
python backend/preprocess_dataset.py
if %ERRORLEVEL% NEQ 0 (
    echo Preprocessing failed. Exiting.
    exit /b %ERRORLEVEL%
)

echo Preprocessing Complete. Starting Training...
python backend/train.py

echo Training Complete.


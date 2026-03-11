
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import model_utils
import config
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize model (lazy loading can also be done)
# Glue code to load model with config paths
# We load the weights if available, otherwise it uses random weights (soft fail)
try:
    model = model_utils.load_trained_model(config.MODEL_WEIGHTS_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Real prediction using the loaded TensorFlow model
        result = model_utils.predict_video(model, filepath)
        
        # Cleanup uploaded file after processing if needed
        # os.remove(filepath)
        
        return jsonify(result)
    except Exception as e:
        print(f"Error processing video: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'Deepfake Detection API is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

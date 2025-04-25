import os
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
from tensorflow import keras
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from flask_cors import CORS
from PIL import Image
import io
import base64
import uuid

from zeroDCE import load_ZeroDCE_model, infer_zerodce
from mirnet import load_mirnet_model, infer_mirnet

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Global zeroDCE_model instance
zeroDCE_model = load_ZeroDCE_model()
mirnet_model = load_mirnet_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Zero-DCE API is running'})

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename to prevent overwriting
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            
            # Save original image
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(original_path)
            
            # Open the saved image for processing
            image = Image.open(original_path)
            
            # # Preprocess the image
            # img_array = keras.utils.img_to_array(image)
            # img_array = img_array.astype("float32") / 255.0
            # img_array = np.expand_dims(img_array, axis=0)
            
            # # Perform inference
            # enhanced_array = model(img_array)
            # enhanced_array = tf.cast((enhanced_array[0, :, :, :] * 255), dtype=np.uint8)
            # enhanced_image = Image.fromarray(enhanced_array.numpy())

            # Enhance image 
            enhanced_image = infer_zerodce(image, zeroDCE_model)
            enhance_image02 = infer_mirnet(image, mirnet_model)
            
            # Save enhanced image of zeroDCE 
            enhanced_filename = f"zerodce_enhanced_{unique_filename}"
            enhanced_path = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename)
            enhanced_image.save(enhanced_path)

            # Save enhanced image of mirnet 
            enhanced_filename02 = f"mirnet_enhanced_{unique_filename}"
            enhanced_path02 = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename02)
            enhance_image02.save(enhanced_path02)

            # Create URLs for the images
            original_url = f"/uploads/{unique_filename}"
            enhanced_url = f"/uploads/{enhanced_filename}"
            enhanced_url02 = f"/uploads/{enhanced_filename02}"

            
            # Return proper JSON with full URLs
            return jsonify({
                'status': 'success',
                'original': original_url,
                'enhanced': enhanced_url,
                'enhanced1': enhanced_url,  # Added for compatibility with frontend
                'enhanced2': enhanced_url02   # Added for compatibility with frontend
            })
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return jsonify({'error': str(e), 'details': 'Error during image processing'}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        # Get the image from the request
        image_file = request.files['image']
        image = Image.open(image_file)
        
        # Preprocess the image
        img_array = keras.utils.img_to_array(image)
        img_array = img_array.astype("float32") / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Perform inference
        enhanced_array = model(img_array)
        enhanced_array = tf.cast((enhanced_array[0, :, :, :] * 255), dtype=np.uint8)
        enhanced_image = Image.fromarray(enhanced_array.numpy())
        
        # Save the enhanced image with a unique name
        filename = secure_filename(image_file.filename)
        file_ext = os.path.splitext(filename)[1]
        enhanced_filename = f"enhanced_{uuid.uuid4().hex}{file_ext}"
        enhanced_path = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename)
        enhanced_image.save(enhanced_path)
        
        # Return the URL to the saved enhanced image
        return jsonify({
            'status': 'success', 
            'enhanced_image': f"/uploads/{enhanced_filename}"
        })
    
    except Exception as e:
        print(f"Error in enhance_image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or use 5000 as default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Set debug=True to see detailed errors
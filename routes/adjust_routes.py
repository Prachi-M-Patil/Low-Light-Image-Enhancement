from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os, uuid
import numpy as np
import cv2
from PIL import Image
from config import Config

adjust_bp = Blueprint('adjust', __name__)

@adjust_bp.route('/brightness_contrast', methods=['POST'])
def adjust_brightness_contrast():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    brightness = int(request.form.get('brightness', 0))
    contrast = int(request.form.get('contrast', 0))

    # Clamp values
    brightness = max(-100, min(100, brightness))
    contrast = max(-100, min(100, contrast))

    image = Image.open(file).convert('RGB')
    img_np = np.array(image)

    alpha = 1 + contrast / 100.0
    beta = brightness
    adjusted = cv2.convertScaleAbs(img_np, alpha=alpha, beta=beta)

    ext = os.path.splitext(secure_filename(file.filename))[1]
    filename = f"adjusted_{uuid.uuid4().hex}{ext}"
    path = os.path.join(Config.ADJUSTED_FOLDER, filename)
    cv2.imwrite(path, adjusted)

    return jsonify({'status': 'success', 'adjusted_image': f"/{path}"})



# @app.route('/adjust_brightness_contrast', methods=['POST'])
# def adjust_brightness_contrast_route():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400

#     try:
#         image_file = request.files['image']
#         brightness = int(request.form.get('brightness', 0))
#         contrast = int(request.form.get('contrast', 0))

#         # Clamp brightness and contrast
#         brightness = max(-100, min(100, brightness))
#         contrast = max(-100, min(100, contrast))

#         # Read image using PIL and convert to NumPy array
#         img = Image.open(image_file).convert('RGB')
#         img_np = np.array(img)

#         # Apply contrast and brightness adjustment
#         alpha = 1 + contrast / 100.0
#         beta = brightness
#         adjusted = cv2.convertScaleAbs(img_np, alpha=alpha, beta=beta)

#         # Save adjusted image
#         file_ext = os.path.splitext(secure_filename(image_file.filename))[1]
#         adjusted_filename = f"adjusted_{uuid.uuid4().hex}{file_ext}"
#         adjusted_path = os.path.join(ADJUSTED_FOLDER, adjusted_filename)
#         cv2.imwrite(adjusted_path, adjusted)

#         return jsonify({
#             'status': 'success',
#             'adjusted_image': f"/{adjusted_path}"
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

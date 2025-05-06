from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os, uuid
from PIL import Image
from config import Config
from utils.filters import (
    apply_gaussian_blur_cv,
    apply_median_blur_cv,
    apply_clahe,
    apply_histogram_equalization_yuv
)

filter_bp = Blueprint('filters', __name__)

def save_filtered_image(image, prefix, filename):
    ext = os.path.splitext(secure_filename(filename))[1]
    filtered_filename = f"{prefix}_{uuid.uuid4().hex}{ext}"
    filtered_path = os.path.join(Config.FILTERED_FOLDER, filtered_filename)
    image.save(filtered_path)
    return filtered_filename

@filter_bp.route('/filter/gaussian', methods=['POST'])
def gaussian_blur():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    kernel_size = int(request.form.get('kernel_size', 5))
    image = Image.open(file)
    result = apply_gaussian_blur_cv(image, kernel_size)
    filename = save_filtered_image(result, 'gaussian', file.filename)

    return jsonify({'status': 'success', 'filtered_image': f"/filtered_images/{filename}"})


@filter_bp.route('/filter/median', methods=['POST'])
def median_blur():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    kernel_size = int(request.form.get('kernel_size', 3))
    image = Image.open(file)
    result = apply_median_blur_cv(image, kernel_size)
    filename = save_filtered_image(result, 'median', file.filename)

    return jsonify({'status': 'success', 'filtered_image': f"/filtered_images/{filename}"})


@filter_bp.route('/filter/hist_eq_yuv', methods=['POST'])
def hist_eq_yuv():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    image = Image.open(file)
    result = apply_histogram_equalization_yuv(image)
    filename = save_filtered_image(result, 'hist_eq', file.filename)

    return jsonify({'status': 'success', 'filtered_image': f"/filtered_images/{filename}"})


@filter_bp.route('/filter/clahe', methods=['POST'])
def clahe():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    clip_limit = float(request.form.get('clip_limit', 2.0))
    grid_size = int(request.form.get('grid_size', 8))

    image = Image.open(file)
    result = apply_clahe(image, clip_limit=clip_limit, tile_grid_size=(grid_size, grid_size))
    filename = save_filtered_image(result, 'clahe', file.filename)

    return jsonify({'status': 'success', 'filtered_image': f"/filtered_images/{filename}"})


# @app.route('/filter/gaussian', methods=['POST'])
# def filter_gaussian():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400
    
#     try:
#         image_file = request.files['image']
#         kernel_size = int(request.form.get('kernel_size', 5))

#         image = Image.open(image_file)
#         blurred_image = apply_gaussian_blur_cv(image, kernel_size)

#         file_ext = os.path.splitext(secure_filename(image_file.filename))[1]
#         filtered_filename = f"gaussian_{uuid.uuid4().hex}{file_ext}"
#         filtered_path = os.path.join(FILTERED_FOLDER, filtered_filename)
#         blurred_image.save(filtered_path)

#         return jsonify({
#             'status': 'success',
#             'filtered_image': f"/{FILTERED_FOLDER}/{filtered_filename}"
#         })
    

#     except Exception as e:
#         print(f"Error in Gaussian filter: {str(e)}")
#         return jsonify({'error': str(e)}), 500


# @app.route('/filter/median', methods=['POST'])
# def filter_median():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400
    
#     try:
#         image_file = request.files['image']
#         kernel_size = int(request.form.get('kernel_size', 3))

#         image = Image.open(image_file)
#         blurred_image = apply_median_blur_cv(image, kernel_size)

#         file_ext = os.path.splitext(secure_filename(image_file.filename))[1]
#         filtered_filename = f"median_{uuid.uuid4().hex}{file_ext}"
#         filtered_path = os.path.join(FILTERED_FOLDER, filtered_filename)
#         blurred_image.save(filtered_path)

#         return jsonify({
#             'status': 'success',
#             'filtered_image': f"/{FILTERED_FOLDER}/{filtered_filename}"
#         })

#     except Exception as e:
#         print(f"Error in Median filter: {str(e)}")
#         return jsonify({'error': str(e)}), 500
    

# @app.route('/filter/hist_eq_yuv', methods=['POST'])
# def filter_hist_eq_yuv():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400
    
#     try:
#         image_file = request.files['image']
#         image = Image.open(image_file)

#         processed_image = apply_histogram_equalization_yuv(image)

#         file_ext = os.path.splitext(secure_filename(image_file.filename))[1]
#         filename = f"hist_eq_{uuid.uuid4().hex}{file_ext}"
#         output_path = os.path.join(FILTERED_FOLDER, filename)
#         processed_image.save(output_path)

#         return jsonify({'status': 'success', 'filtered_image': f"/{FILTERED_FOLDER}/{filename}"})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    

# @app.route('/filter/clahe', methods=['POST'])
# def filter_clahe():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400
    
#     try:
#         image_file = request.files['image']
#         clip_limit = float(request.form.get('clip_limit', 2.0))
#         grid_size = int(request.form.get('grid_size', 8))
#         image = Image.open(image_file)

#         processed_image = apply_clahe(image, clip_limit=clip_limit, tile_grid_size=(grid_size, grid_size))

#         file_ext = os.path.splitext(secure_filename(image_file.filename))[1]
#         filename = f"clahe_{uuid.uuid4().hex}{file_ext}"
#         output_path = os.path.join(FILTERED_FOLDER, filename)
#         processed_image.save(output_path)

#         return jsonify({'status': 'success', 'filtered_image': f"/{FILTERED_FOLDER}/{filename}"})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

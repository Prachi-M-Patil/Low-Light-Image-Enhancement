from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os, uuid
from PIL import Image
from config import Config
from models.zeroDCE import load_ZeroDCE_model, infer_zerodce
from models.mirnet import load_mirnet_model, infer_mirnet

enhance_bp = Blueprint('enhance', __name__)
zeroDCE_model = load_ZeroDCE_model()
mirnet_model = load_mirnet_model()

@enhance_bp.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        original_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        file.save(original_path)

        image = Image.open(original_path)

        # Run both models
        enhanced_image_1 = infer_zerodce(image, zeroDCE_model)
        enhanced_image_2 = infer_mirnet(image, mirnet_model)

        # Save outputs
        path_1 = os.path.join(Config.UPLOAD_FOLDER, f"zerodce_enhanced_{unique_filename}")
        path_2 = os.path.join(Config.UPLOAD_FOLDER, f"mirnet_enhanced_{unique_filename}")
        enhanced_image_1.save(path_1)
        enhanced_image_2.save(path_2)

        return jsonify({
            'status': 'success',
            'original': f"/uploads/{unique_filename}",
            'enhanced1': f"/uploads/zerodce_enhanced_{unique_filename}",
            'enhanced2': f"/uploads/mirnet_enhanced_{unique_filename}"
        })

    return jsonify({'error': 'Invalid file'}), 400


# @app.route('/process_image', methods=['POST'])
# def process_image():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     if file and allowed_file(file.filename):
#         try:
#             # Generate unique filename to prevent overwriting
#             filename = secure_filename(file.filename)
#             file_ext = os.path.splitext(filename)[1]
#             unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            
#             # Save original image
#             original_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
#             file.save(original_path)
            
#             # Open the saved image for processing
#             image = Image.open(original_path)
            
#             # # Preprocess the image
#             # img_array = keras.utils.img_to_array(image)
#             # img_array = img_array.astype("float32") / 255.0
#             # img_array = np.expand_dims(img_array, axis=0)
            
#             # # Perform inference
#             # enhanced_array = model(img_array)
#             # enhanced_array = tf.cast((enhanced_array[0, :, :, :] * 255), dtype=np.uint8)
#             # enhanced_image = Image.fromarray(enhanced_array.numpy())

#             # Enhance image 
#             enhanced_image = infer_zerodce(image, zeroDCE_model)
#             enhance_image02 = infer_mirnet(image, mirnet_model)
            
#             # Save enhanced image of zeroDCE 
#             enhanced_filename = f"zerodce_enhanced_{unique_filename}"
#             enhanced_path = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename)
#             enhanced_image.save(enhanced_path)

#             # Save enhanced image of mirnet 
#             enhanced_filename02 = f"mirnet_enhanced_{unique_filename}"
#             enhanced_path02 = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename02)
#             enhance_image02.save(enhanced_path02)

#             # Create URLs for the images
#             original_url = f"/uploads/{unique_filename}"
#             enhanced_url = f"/uploads/{enhanced_filename}"
#             enhanced_url02 = f"/uploads/{enhanced_filename02}"

            
#             # Return proper JSON with full URLs
#             return jsonify({
#                 'status': 'success',
#                 'original': original_url,
#                 'enhanced': enhanced_url,
#                 'enhanced1': enhanced_url,  # Added for compatibility with frontend
#                 'enhanced2': enhanced_url02   # Added for compatibility with frontend
#             })
            
#         except Exception as e:
#             print(f"Error processing image: {str(e)}")
#             return jsonify({'error': str(e), 'details': 'Error during image processing'}), 500
        
#     return jsonify({'error': 'File type not allowed'}), 400

# @app.route('/enhance', methods=['POST'])
# def enhance_image():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400
    
#     try:
#         # Get the image from the request
#         image_file = request.files['image']
#         image = Image.open(image_file)
        
#         # Preprocess the image
#         img_array = keras.utils.img_to_array(image)
#         img_array = img_array.astype("float32") / 255.0
#         img_array = np.expand_dims(img_array, axis=0)
        
#         # Perform inference
#         enhanced_array = model(img_array)
#         enhanced_array = tf.cast((enhanced_array[0, :, :, :] * 255), dtype=np.uint8)
#         enhanced_image = Image.fromarray(enhanced_array.numpy())
        
#         # Save the enhanced image with a unique name
#         filename = secure_filename(image_file.filename)
#         file_ext = os.path.splitext(filename)[1]
#         enhanced_filename = f"enhanced_{uuid.uuid4().hex}{file_ext}"
#         enhanced_path = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename)
#         enhanced_image.save(enhanced_path)
        
#         # Return the URL to the saved enhanced image
#         return jsonify({
#             'status': 'success', 
#             'enhanced_image': f"/uploads/{enhanced_filename}"
#         })
    
#     except Exception as e:
#         print(f"Error in enhance_image: {str(e)}")
#         return jsonify({'error': str(e)}), 500
    

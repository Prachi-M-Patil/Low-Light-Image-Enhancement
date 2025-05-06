import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    FILTERED_FOLDER = 'filtered_images'
    ADJUSTED_FOLDER = 'adjusted_images'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Ensure folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(FILTERED_FOLDER, exist_ok=True)
    os.makedirs(ADJUSTED_FOLDER, exist_ok=True)

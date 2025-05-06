# filters.py
import cv2
import numpy as np
from PIL import Image

# Smoothing filters

def read_image_as_array(image: Image.Image) -> np.ndarray:
    if image.mode in ('RGBA', 'LA'):
        image = image.convert("RGB")
    elif image.mode != 'RGB':
        image = image.convert("RGB")
    return np.array(image)

def apply_gaussian_blur_cv(image: Image.Image, kernel_size: int) -> Image.Image:
    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be an odd number.")
    img_array = read_image_as_array(image)
    blurred = cv2.GaussianBlur(img_array, (kernel_size, kernel_size), sigmaX=0)
    return Image.fromarray(blurred)

def apply_median_blur_cv(image: Image.Image, kernel_size: int) -> Image.Image:
    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be an odd number.")
    img_array = read_image_as_array(image)
    blurred = cv2.medianBlur(img_array, kernel_size)
    return Image.fromarray(blurred)


# sharpening filters
def apply_sharpening(image: Image.Image) -> Image.Image:
    """
    Applies a basic sharpening kernel using convolution.
    """
    img_array = read_image_as_array(image)
    
    # Define a sharpening kernel
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    
    # Apply the kernel to the image
    sharpened = cv2.filter2D(img_array, -1, kernel)
    
    return Image.fromarray(sharpened)


def apply_histogram_equalization_yuv(image: Image.Image) -> Image.Image:
    img_array = read_image_as_array(image)
    img_yuv = cv2.cvtColor(img_array, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])  # Equalize the Y (luminance) channel
    equalized_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return Image.fromarray(equalized_img)

def apply_clahe(image: Image.Image, clip_limit=2.0, tile_grid_size=(8, 8)) -> Image.Image:
    img_array = read_image_as_array(image)
    img_lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(img_lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    final = cv2.cvtColor(merged, cv2.COLOR_LAB2RGB)
    return Image.fromarray(final)

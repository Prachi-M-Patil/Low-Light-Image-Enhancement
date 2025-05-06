import cv2
import numpy as np
import os
import uuid

def adjust_brightness_contrast_preserve_color(img_np, brightness=0, contrast=0, output_dir='static/filtered_images'):
    # Clamp values
    brightness = np.clip(brightness, -100, 100)
    contrast = np.clip(contrast, -100, 100)

    # Convert to HSV
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV).astype(np.float32)

    # Adjust brightness (Value channel)
    v = hsv[:, :, 2]
    v = v + brightness
    v = np.clip(v, 0, 255)

    # Optional: Adjust contrast (simple method by stretching)
    if contrast != 0:
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        v = 128 + factor * (v - 128)
        v = np.clip(v, 0, 255)

    hsv[:, :, 2] = v

    # Convert back to RGB
    adjusted_rgb = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    # Save image
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"adjusted_{uuid.uuid4().hex}.png"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, cv2.cvtColor(adjusted_rgb, cv2.COLOR_RGB2BGR))

    return output_path

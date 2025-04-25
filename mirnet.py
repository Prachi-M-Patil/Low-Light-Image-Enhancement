# mirnet_model.py

from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import activations
from tensorflow.keras.models import load_model
from keras import layers

class ChannelPooling(layers.Layer):
    def __init__(self, axis=-1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axis = axis
        self.concat = layers.Concatenate(axis=self.axis)

    def build(self, input_shape):
        # Nothing to build, but this silences the warning
        super().build(input_shape)

    def call(self, inputs):
        avg_pool = tf.expand_dims(tf.reduce_mean(inputs, axis=-1), axis=-1)
        max_pool = tf.expand_dims(tf.reduce_max(inputs, axis=-1), axis=-1)
        return self.concat([avg_pool, max_pool])

    def get_config(self):
        config = super().get_config()
        config.update({"axis": self.axis})
        return config
    

def load_mirnet_model(model_path='mirnet_model.keras'):
    print("Loading MIRNet model...")
    model = load_model(
        model_path,
        custom_objects={
            'ChannelPooling': ChannelPooling,
            'sigmoid': activations.sigmoid
        }
    )
    print("MIRNet model loaded successfully!")
    return model



# def infer_mirnet(image: Image.Image, model) -> Image.Image:
#     image_array = keras.utils.img_to_array(image)
#     image_array = image_array.astype("float32") / 255.0
#     image_array = np.expand_dims(image_array, axis=0)
    
#     output = model.predict(image_array, verbose=0)
#     output_image = output[0] * 255.0
#     output_image = output_image.clip(0, 255)
#     output_image = Image.fromarray(np.uint8(output_image))
    
#     return output_image


def infer_mirnet(original_image: Image.Image, model) -> Image.Image:
    # Get original dimensions
    width, height = original_image.size

    # Ensure both dimensions are even
    width_even = width if width % 2 == 0 else width - 1
    height_even = height if height % 2 == 0 else height - 1

    # Resize image to even dimensions
    resized_image = original_image.resize((width_even, height_even))

    # Preprocess
    img_array = keras.utils.img_to_array(resized_image).astype("float32") / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    output = model.predict(img_array, verbose=0)
    output_image = output[0] * 255.0
    output_image = output_image.clip(0, 255).astype("uint8")

    return Image.fromarray(output_image)


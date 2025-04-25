# ZeroDCE Model class

from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras

class ZeroDCE(keras.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dce_model = self.build_dce_net()

    def build_dce_net(self):
        input_img = keras.Input(shape=[None, None, 3])
        conv1 = keras.layers.Conv2D(32, (3, 3), strides=(1, 1), activation="relu", padding="same")(input_img)
        conv2 = keras.layers.Conv2D(32, (3, 3), strides=(1, 1), activation="relu", padding="same")(conv1)
        conv3 = keras.layers.Conv2D(32, (3, 3), strides=(1, 1), activation="relu", padding="same")(conv2)
        conv4 = keras.layers.Conv2D(32, (3, 3), strides=(1, 1), activation="relu", padding="same")(conv3)
        int_con1 = keras.layers.Concatenate(axis=-1)([conv4, conv3])
        conv5 = keras.layers.Conv2D(32, (3, 3), strides=(1, 1), activation="relu", padding="same")(int_con1)
        int_con2 = keras.layers.Concatenate(axis=-1)([conv5, conv2])
        conv6 = keras.layers.Conv2D(32, (3, 3), strides=(1, 1), activation="relu", padding="same")(int_con2)
        int_con3 = keras.layers.Concatenate(axis=-1)([conv6, conv1])
        x_r = keras.layers.Conv2D(24, (3, 3), strides=(1, 1), activation="tanh", padding="same")(int_con3)
        return keras.Model(inputs=input_img, outputs=x_r)

    def get_enhanced_image(self, data, output):
        r = [output[:, :, :, i*3:(i+1)*3] for i in range(8)]
        x = data
        for ri in r:
            x = x + ri * (tf.square(x) - x)
        return x

    def call(self, data):
        dce_net_output = self.dce_model(data)
        return self.get_enhanced_image(data, dce_net_output)



def load_ZeroDCE_model(weights_path='modelZeroDCE.h5'):
    print("Loading Zero-DCE model...")
    model = ZeroDCE()
    
    # Build the model with a dummy input
    dummy_input = tf.ones((1, 64, 64, 3))
    _ = model(dummy_input)
    
    # Load pre-trained weights
    model.load_weights(weights_path)
    
    print("Model loaded successfully!")
    return model


def infer_zerodce(image: Image.Image, model) -> Image.Image:
    # Convert to array and normalize
    img_array = keras.utils.img_to_array(image)
    img_array = img_array.astype("float32") / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Run model inference
    enhanced_array = model(img_array)

    # Convert back to image
    enhanced_array = tf.cast((enhanced_array[0] * 255), dtype=tf.uint8)
    enhanced_image = Image.fromarray(enhanced_array.numpy())

    return enhanced_image

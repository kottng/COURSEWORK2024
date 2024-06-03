import tensorflow as tf
from tensorflow.keras.models import load_model

# Define a custom Lambda layer class to override from_config method
class CustomLambda(tf.keras.layers.Lambda):
    def from_config(cls, config):
        return cls(lambda x: x, **config)

# Load the model with safe_mode=False
model = load_model("CourseWorkModel.keras", safe_mode=False)

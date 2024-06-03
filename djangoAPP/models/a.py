from tensorflow.keras.models import load_model

# Enable unsafe deserialization globally
import keras
keras.utils.get_custom_objects().update({"safe_mode": False})

# Load the model with safe_mode=False
model = load_model("CourseWorkModel.keras", custom_objects={"safe_mode": False})

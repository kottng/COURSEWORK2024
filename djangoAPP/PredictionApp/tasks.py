import os
from io import BytesIO
import numpy as np
from PIL import Image as PILImage
from skimage.transform import resize
import tensorflow as tf
from celery import shared_task
from django.core.files.storage import default_storage
from .models import PlantPhoto, PlantAnalytics
from .yandex_storage import YandexDiskStorage
import requests

@shared_task
def process_photo(photo_id):
    photo = PlantPhoto.objects.get(id=photo_id)
    fileObj = photo.photo
    fs = YandexDiskStorage()
    response = requests.get(fileObj.url)
    img = PILImage.open(BytesIO(response.content))
    IMG_WIDTH = 128
    IMG_HEIGHT = 128
    IMG_CHANNELS = 3
    X_user_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
    img = np.array(img)
    img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
    X_user_test[0] = img
    model = tf.keras.models.load_model("/home/vboxuser/Desktop/CourseWork2024FINAL/backend/djangoAPP/models/CourseWorkModel.keras", safe_mode=False)
    preds_user_test = model.predict(X_user_test, verbose=1)
    preds_user_test_t = (preds_user_test > 0.5).astype(np.uint8)
    arr = (np.squeeze(preds_user_test_t[0]) * 255).astype(np.uint8)
    processed_image = PILImage.fromarray(arr)
    processed_image_name = "processed_" + fileObj.name
    processed_image_io = BytesIO()
    processed_image.save(processed_image_io, format='PNG')
    processed_image_io.seek(0)
    fs._save(processed_image_name, processed_image_io)
    processed_image_url = fs.url(processed_image_name)
    plant_analytics, created = PlantAnalytics.objects.get_or_create(plant_photo=photo)
    plant_analytics.plant_photo_processed = processed_image_url
    plant_analytics.save()
    return processed_image_url


# from __future__ import absolute_import, unicode_literals
# from celery import shared_task
# import tensorflow as tf
# import numpy as np
# from PIL import Image as PILImage
# from django.core.files.storage import FileSystemStorage
# from skimage.transform import resize
# from .models import PlantPhoto, PlantAnalytics
# import os
# from .yandex_storage import YandexDiskStorage
# import io
# import requests


# @shared_task
# def process_photo(photo_id):
#     photo = PlantPhoto.objects.get(id=photo_id)
#     fileObj = photo.photo
#     fs = YandexDiskStorage()
    
#     # Download the original photo
#     response = requests.get(fileObj.url)
#     img = PILImage.open(io.BytesIO(response.content))
    
#     IMG_WIDTH = 128
#     IMG_HEIGHT = 128
#     IMG_CHANNELS = 3

#     X_user_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
#     img = np.array(img)
#     img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
#     X_user_test[0] = img

#     model = tf.keras.models.load_model("/home/vboxuser/Desktop/CourseWork2024FINAL/backend/djangoAPP/models/CourseWorkModel.keras", safe_mode=False)
#     preds_user_test = model.predict(X_user_test, verbose=1)
#     preds_user_test_t = (preds_user_test > 0.5).astype(np.uint8)
#     arr = (np.squeeze(preds_user_test_t[0]) * 255).astype(np.uint8)
#     processed_image = PILImage.fromarray(arr)

#     processed_image_name = "processed_" + fileObj.name
#     processed_image_path = os.path.join(fs.root_path, processed_image_name)
#     processed_image_io = io.BytesIO()
#     processed_image.save(processed_image_io, format='PNG')
#     processed_image_io.seek(0)
    
#     fs._save(processed_image_name, processed_image_io)

#     processed_image_url = fs.url(processed_image_name)

#     plant_analytics, created = PlantAnalytics.objects.get_or_create(plant_photo=photo)
#     plant_analytics.plant_photo_processed = processed_image_url
#     plant_analytics.save()

#     return processed_image_url


# @shared_task
# def process_photo(photo_id):
#     photo = PlantPhoto.objects.get(id=photo_id)
#     fileObj = photo.photo
#     fs = FileSystemStorage()
#     filePathName = fs.save(fileObj.name, fileObj)

#     IMG_WIDTH = 128
#     IMG_HEIGHT = 128
#     IMG_CHANNELS = 3
#     test_user_image_dir = fs.location
#     user_image_files = os.listdir(test_user_image_dir)

#     X_user_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
    
#     img_path = os.path.join(test_user_image_dir, user_image_files[0])
#     img = PILImage.open(fileObj)
#     img = np.array(img)
#     img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
#     X_user_test[0] = img
    
#     model = tf.keras.models.load_model("/home/vboxuser/Desktop/CourseWork2024FINAL/backend/djangoAPP/models/CourseWorkModel.keras", safe_mode=False)
#     preds_user_test = model.predict(X_user_test, verbose=1)
#     preds_user_test_t = (preds_user_test > 0.5).astype(np.uint8)
#     arr = (np.squeeze(preds_user_test_t[0]) * 255).astype(np.uint8)
#     processed_image = PILImage.fromarray(arr)

#     processed_image_name = "processed_" + fileObj.name
#     processed_image_path = os.path.join(test_user_image_dir, processed_image_name)
#     processed_image.save(processed_image_path)
#     processed_image_url = fs.url(processed_image_name)

#     plant_analytics, created = PlantAnalytics.objects.get_or_create(plant_photo=photo)
#     plant_analytics.plant_photo_processed = processed_image_url
#     plant_analytics.save()
#     print("this is the processed image url", processed_image_url)

#     return processed_image_url

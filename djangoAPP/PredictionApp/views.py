from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Plant
from .models import ArchiveNote
from .models import PlantPhoto
from .forms import PlantForm
# from .forms import ImageForm
from .forms import CreateUserForm
from .forms import LoginForm
from .forms import ArchiveNoteForm
from .forms import PlantPhotoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
import os
import numpy as np
from PIL import Image as PILImage
from skimage.transform import resize
from tqdm import tqdm
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from celery import Celery

from django.db.models import Q

@login_required(login_url="my-login")
def Plants(request):
    start_date = request.GET.get('startDate', None)
    end_date = request.GET.get('endDate', None)
    variety = request.GET.get('variety', None)
    search_id = request.GET.get('search_id', None)
    plants = Plant.objects.all()

    if start_date:
        plants = plants.filter(planting_date__gte=start_date)
    if end_date:
        plants = plants.filter(planting_date__lte=end_date)
    if variety:
        plants = plants.filter(variety=variety)
    if search_id:
        plants = plants.filter(id=search_id)
    print(search_id)

    context = {
        'form': plants,
        'plant_varieties': Plant.objects.values_list('variety', flat=True).distinct()
    }
    return render(request, "PredictionApp/index.html", context)


@login_required(login_url="my-login")
def viewPlant(request, id):
    form = get_object_or_404(Plant, id=id)
    archive_notes = ArchiveNote.objects.filter(plant_id=id)
    
    # Apply date filters
    start_date = request.GET.get('startDate', None)
    end_date = request.GET.get('endDate', None)
    if start_date:
        archive_notes = archive_notes.filter(date_taken__gte=start_date)
    if end_date:
        archive_notes = archive_notes.filter(date_taken__lte=end_date)
    
    context = {'form': form, 'archive_notes': archive_notes}
    return render(request, "PredictionApp/viewPlant.html", context)



# def test(request):
#     return render(request, "PredictionApp/test.html")


import os
import numpy as np
from PIL import Image as PILImage
from skimage.transform import resize
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tqdm import tqdm
from .models import Plant
import tensorflow as tf
import requests

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import ArchiveNote, PlantPhoto, PlantAnalytics
from .tasks import process_photo

@login_required(login_url="my-login")
def viewPhotoAnalytics(request, id):
    try:
        archive_note = ArchiveNote.objects.get(id=id)
        photos_archive_note = archive_note.photo.all()

        for photo in photos_archive_note:
            process_photo.delay(photo.id)

        return render(request, 'PredictionApp/viewPhotoAnalytics.html', {
            'archive_note': archive_note,
            'processed_photos': []
        })

    except Exception as e:
        print("exception of photo analytics is", e)
        return JsonResponse({'success': False})

def get_processed_photos(request, archive_note_id):
    archive_note = get_object_or_404(ArchiveNote, id=archive_note_id)
    photos = archive_note.photo.all()
    processed_photos = []
    
    for photo in photos:
        try:
            analytics = PlantAnalytics.objects.get(plant_photo=photo)
            processed_image_url = analytics.plant_photo_processed.url if analytics.plant_photo_processed else ''
        except PlantAnalytics.DoesNotExist:
            print("processed image was not found")
            processed_image_url = ''
        
        processed_photos.append({
            'original_image_url': photo.photo.url,
            'processed_image_url': processed_image_url,
        })
    
    return JsonResponse({'processed_photos': processed_photos})

@login_required(login_url="my-login")
def viewArchiveNote(request, id):
    archive_note = ArchiveNote.objects.get(id=id)
    if request.method == 'POST':
        PhotoForm = PlantPhotoForm(request.POST, request.FILES)
        if PhotoForm.is_valid():
            for i in PhotoForm.cleaned_data["photo"]:
                PlantPhoto.objects.create(archiveNote=archive_note, photo=i)
            messages.success(request, "Plant added successfully")
            return render(request, 'PredictionApp/viewArchiveNote.html', {'PhotoForm': PhotoForm, 'archive_note': archive_note})
        else:
            print("there is an error")
    else:
        PhotoForm = PlantPhotoForm()
        return render(request, 'PredictionApp/viewArchiveNote.html', {'PhotoForm': PhotoForm, 'archive_note': archive_note})

@login_required(login_url="my-login")
def addArchiveNote(request, id):
    if request.method == 'POST':
        form = ArchiveNoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Archive note added successfully")
            return render(request, 'PredictionApp/addArchiveNote.html', {'form': form})
    else:
        form = ArchiveNoteForm(initial={'plant': id})
        return render(request, 'PredictionApp/addArchiveNote.html', {'form': form})

def addPlant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Plant added successfully")
            img_obj = form.instance
            return render(request, 'PredictionApp/addPlant.html', {'form': form, 'img_obj': img_obj})
    else:
        form = PlantForm()
        return render(request, 'PredictionApp/addPlant.html', {'form': form})

@login_required(login_url="my-login")
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect('Plants')

@login_required(login_url="my-login")
def deleteArchiveNote(request, id):
    archive_note = get_object_or_404(ArchiveNote, id=id)
    plant_id = archive_note.plant.id
    archive_note.delete()
    return redirect('viewPlant', id=plant_id)





# @login_required(login_url="my-login")
# def viewPhotoAnalytics(request, id):
#     try:
#         archive_note = ArchiveNote.objects.get(id=id)
#         photos_archive_note = archive_note.photo.all()

#         for photo in photos_archive_note:
#             process_photo.delay(photo.id)  # Use Celery task

#         return render(request, 'PredictionApp/viewPhotoAnalytics.html', {
#             'archive_note': archive_note,
#             'processed_photos': []  # We will handle this in a more dynamic way later
#         })

#     except Exception as e:
#         print("exception of photo analytics is", e)
#         return JsonResponse({'success': False})

# def get_processed_photos(request, archive_note_id):
#     archive_note = get_object_or_404(ArchiveNote, id=archive_note_id)
#     photos = archive_note.photo.all()
#     processed_photos = []
    
#     for photo in photos:
#         try:
#             analytics = PlantAnalytics.objects.get(plant_photo=photo)
#             processed_image_url = analytics.plant_photo_processed.url if analytics.plant_photo_processed else ''
#         except PlantAnalytics.DoesNotExist:
#             print("processed image was not found")
#             processed_image_url = ''
        
#         processed_photos.append({
#             'original_image_url': photo.photo.url,
#             'processed_image_url': processed_image_url,
#         })
    
#     return JsonResponse({'processed_photos': processed_photos})


# @login_required(login_url="my-login")
# def viewArchiveNote(request, id):
#     archive_note = ArchiveNote.objects.get(id=id)
#     if request.method == 'POST':
#         PhotoForm = PlantPhotoForm(request.POST, request.FILES)
#         if PhotoForm.is_valid():
#             for i in PhotoForm.cleaned_data["photo"]:
#                 PlantPhoto.objects.create(archiveNote=archive_note, photo=i)
#             messages.success(request, "PLant added Succesfully")
#             return render(request, 'PredictionApp/viewArchiveNote.html', {'PhotoForm': PhotoForm, 'archive_note': archive_note})
#         else:
#             print("there is an error")
#     else:
#         PhotoForm = PlantPhotoForm()
#         return render(request, 'PredictionApp/viewArchiveNote.html', {'PhotoForm': PhotoForm, 'archive_note': archive_note})
    

# @login_required(login_url="my-login")
# def addArchiveNote(request, id):
#     if request.method == 'POST':
#         form = ArchiveNoteForm(request.POST)
#         print(form)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Archive note added Succesfully")
#             return render(request, 'PredictionApp/addArchiveNote.html', {'form': form})
#     else:
#         form = ArchiveNoteForm(initial={'plant': id})
#         return render(request, 'PredictionApp/addArchiveNote.html', {'form': form})

# @login_required(login_url="my-login")
# def addPlant(request):
#     if request.method == 'POST':
#         form = PlantForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Plant added Succesfully")
#             img_obj = form.instance
#             return render(request, 'PredictionApp/addPlant.html', {'form': form, 'img_obj': img_obj})
#     else:
#         form = PlantForm()
#         return render(request, 'PredictionApp/addPlant.html', {'form': form})

# from django.shortcuts import get_object_or_404

# @login_required(login_url="my-login")
# def delete_plant(request, plant_id):
#     plant = get_object_or_404(Plant, id=plant_id)
#     plant.delete()
#     return redirect('Plants')

# @login_required(login_url="my-login")
# def deleteArchiveNote(request, id):
#     archive_note = get_object_or_404(ArchiveNote, id=id)
#     plant_id = archive_note.plant.id
#     print(plant_id)
#     archive_note.delete()
#     return redirect('viewPlant', id=plant_id)
    



# not useful part:



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("Plants")


    context = {'loginform':form}

    return render(request, 'PredictionApp/my-login.html', context=context)


@login_required(login_url="my-login")
def myProfile(request):
    form = Plant.objects.all()
    context = {'form':form}
    print(context)
    return render(request, "PredictionApp/myProfile.html", context)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")
    context = {'registerform':form}
    return render(request, 'PredictionApp/register.html', context=context)
    
    
def user_logout(request):

    auth.logout(request)

    return redirect("my-login")

from .forms import UserProfileForm
    
@login_required(login_url="my-login")
def myProfile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile details updated successfully!')
            return redirect('myProfile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, "PredictionApp/myProfile.html", {'form': form})



# @login_required(login_url="my-login")
# def Plants(request):
#     start_date = request.GET.get('startDate', None)
#     end_date = request.GET.get('endDate', None)
#     variety = request.GET.get('variety', None)
#     search_id = request.GET.get('search_id', None)
#     plants = Plant.objects.all()

#     if start_date:
#         plants = plants.filter(planting_date__gte=start_date)
#     if end_date:
#         plants = plants.filter(planting_date__lte=end_date)
#     if variety:
#         plants = plants.filter(variety=variety)
#     if search_id:
#         plants = plants.filter(id=search_id)
#     print(search_id)

#     context = {
#         'form': plants,
#         'plant_varieties': Plant.objects.values_list('variety', flat=True).distinct()
#     }
#     return render(request, "PredictionApp/index.html", context)

# @login_required(login_url="my-login")
# def viewPlant(request, id):
#     form = Plant.objects.get(id=id)
#     archive_notes = ArchiveNote.objects.filter(plant_id=id)
    
#     # Apply date filters
#     start_date = request.GET.get('startDate', None)
#     end_date = request.GET.get('endDate', None)
#     if start_date:
#         archive_notes = archive_notes.filter(date_taken__gte=start_date)
#     if end_date:
#         archive_notes = archive_notes.filter(date_taken__lte=end_date)
    
#     context = {'form': form, 'archive_notes': archive_notes}
#     return render(request, "PredictionApp/viewPlant.html", context)





# @login_required(login_url="my-login")
# def viewPhotoAnalytics(request, id):
#     try:
#         archive_note = ArchiveNote.objects.get(id=id)
#         photos_archive_note = archive_note.photo.all()
#         model = tf.keras.models.load_model("/home/vboxuser/Desktop/CourseWork2024FINAL/backend/djangoAPP/models/CourseWorkModel.keras", safe_mode=False)
        
#         processed_photos = []
#         for photo in photos_archive_note:
#             fileObj = photo.photo
#             fs = FileSystemStorage()
#             filePathName = fs.save(fileObj.name, fileObj)
            
#             IMG_WIDTH = 128
#             IMG_HEIGHT = 128
#             IMG_CHANNELS = 3
#             test_user_image_dir = fs.location
#             user_image_files = os.listdir(test_user_image_dir)

#             X_user_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
            
#             img_path = os.path.join(test_user_image_dir, user_image_files[0])
#             img = PILImage.open(fileObj)
#             img = np.array(img)
#             img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
#             X_user_test[0] = img
            
#             preds_user_test = model.predict(X_user_test, verbose=1)
#             preds_user_test_t = (preds_user_test > 0.5).astype(np.uint8)
#             arr = (np.squeeze(preds_user_test_t[0]) * 255).astype(np.uint8)
#             processed_image = PILImage.fromarray(arr)

#             processed_image_name = "processed_" + fileObj.name
#             processed_image_path = os.path.join(test_user_image_dir, processed_image_name)
#             processed_image.save(processed_image_path)
#             processed_image_url = fs.url(processed_image_name)
#             photo.analytics.plant_photo = processed_image_url

#             processed_photos.append({
#                 'original_image_url': fs.url(filePathName),
#                 'processed_image_url': processed_image_url
#             })
            
#             #
#             im = PILImage.open(fileObj)
#             pixels = im.load()
#             x, y = im.size

#             white_pix = 0
#             another_pix = 0

#             for i in range(x):
#                 for j in range(y):

#                     color = pixels[i, j]

#                     flag = True
#                     for q in range(3):
#                         if pixels[i, j][q] == 255:
#                             flag = False

#                     if flag:
#                         white_pix += 1
#                     another_pix += 1
#             print(white_pix)
#             print(another_pix)
#             # 
            
#         return render(request, 'PredictionApp/viewPhotoAnalytics.html', {
#             'archive_note': archive_note,
#             'processed_photos': processed_photos
#         })

#     except Exception as e:
#         print(e)
#         return JsonResponse({'success': False})

# def get_processed_photos(request, archive_note_id):
#     archive_note = ArchiveNote.objects.get(id=archive_note_id)
#     photos = archive_note.photo.all()
#     processed_photos = [
#         {
#             'original_image_url': photo.photo.url,
#             # 'processed_image_url': photo.photo.url if photo.photo else ''
#             'processed_image_url': photo.analytics.plant_photo_processed.url if photo.analytics.plant_photo_processed else ''
#         } for photo in photos
#     ]
#     return JsonResponse({'processed_photos': processed_photos})


# @login_required(login_url="my-login")
# def makeAnalytics(request, id):
#     try:
#         print("IT IS OKEY")
#         form = Plant.objects.get(id=id)
#         archive_notes = ArchiveNote.objects.filter(plant_id=id)
#         print("IT IS OKEY")
#         start_date = request.GET.get('startDate', None)
#         end_date = request.GET.get('endDate', None)
#         if start_date:
#             archive_notes = archive_notes.filter(date_taken__gte=start_date)
#         if end_date:
#             archive_notes = archive_notes.filter(date_taken__lte=end_date)
#         print("IT IS OKEY")
#         processed_photos = []
#         model = tf.keras.models.load_model("/home/vboxuser/Desktop/CourseWork2024FINAL/backend/djangoAPP/models/CourseWorkModel.keras", safe_mode=False)
#         print("IT IS OKEY")
#         for archive_note in archive_notes:
#             photos_archive_note = archive_note.photo.all()
            
#             for photo in photos_archive_note:
#                 fileObj = photo.photo
#                 fs = FileSystemStorage()
#                 filePathName = fs.save(fileObj.name, fileObj)
                
#                 IMG_WIDTH = 128
#                 IMG_HEIGHT = 128
#                 IMG_CHANNELS = 3
#                 test_user_image_dir = fs.location
#                 user_image_files = os.listdir(test_user_image_dir)

#                 X_user_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
                
#                 img_path = os.path.join(test_user_image_dir, user_image_files[0])
#                 img = PILImage.open(fileObj)
#                 img = np.array(img)
#                 img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
#                 X_user_test[0] = img
                
#                 preds_user_test = model.predict(X_user_test, verbose=1)
#                 preds_user_test_t = (preds_user_test > 0.5).astype(np.uint8)
#                 arr = (np.squeeze(preds_user_test_t[0]) * 255).astype(np.uint8)
#                 processed_image = PILImage.fromarray(arr)

#                 processed_image_name = "processed_" + fileObj.name
#                 processed_image_path = os.path.join(test_user_image_dir, processed_image_name)
#                 processed_image.save(processed_image_path)
#                 processed_image_url = fs.url(processed_image_name)
#                 photo.analytics.plant_photo = processed_image_url

#                 processed_photos.append({
#                     'original_image_url': fs.url(filePathName),
#                     'processed_image_url': processed_image_url
#                 })

#                 im = PILImage.open(fileObj)
#                 pixels = im.load()
#                 x, y = im.size

#                 white_pix = 0
#                 another_pix = 0

#                 for i in range(x):
#                     for j in range(y):
#                         color = pixels[i, j]
#                         flag = True
#                         for q in range(3):
#                             if pixels[i, j][q] == 255:
#                                 flag = False
#                         if flag:
#                             white_pix += 1
#                         another_pix += 1

#                 print(white_pix)
#                 print(another_pix)

#         context = {
#             'form': form,
#             'processed_photos': processed_photos
#         }
        
#         return render(request, "PredictionApp/processedPhotos.html", context)
    
#     except Exception as e:
#         print(e) 
#         return JsonResponse({'success': False, 'error': str(e)})




# def viewAnalytics(request, id):
#     try:
#         archive_note = ArchiveNote.objects.get(id=id)
#         photos_archive_note = archive_note.photo.all()
#         model = tf.keras.models.load_model("/home/vboxuser/Desktop/CourseWork2024FINAL/backend/djangoAPP/models/CourseWorkModel.keras", safe_mode=False)
        
#         processed_photos = []
#         for photo in photos_archive_note:
#             fileObj = photo.photo
#             fs = FileSystemStorage()
#             filePathName = fs.save(fileObj.name, fileObj)
            
#             IMG_WIDTH = 128
#             IMG_HEIGHT = 128
#             IMG_CHANNELS = 3
#             test_user_image_dir = fs.location
#             user_image_files = os.listdir(test_user_image_dir)

#             X_user_test = np.zeros((1, IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
            
#             img_path = os.path.join(test_user_image_dir, user_image_files[0])
#             img = PILImage.open(fileObj)
#             img = np.array(img)
#             img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
#             X_user_test[0] = img
            
#             preds_user_test = model.predict(X_user_test, verbose=1)
#             preds_user_test_t = (preds_user_test > 0.5).astype(np.uint8)
#             arr = (np.squeeze(preds_user_test_t[0]) * 255).astype(np.uint8)
#             processed_image = PILImage.fromarray(arr)

#             processed_image_name = "processed_" + fileObj.name
#             processed_image_path = os.path.join(test_user_image_dir, processed_image_name)
#             processed_image.save(processed_image_path)
#             processed_image_url = fs.url(processed_image_name)
#             photo.analytics.plant_photo = processed_image_url

#             processed_photos.append({
#                 'original_image_url': fs.url(filePathName),
#                 'processed_image_url': processed_image_url
#             })
#             im = PILImage.open(fileObj)
#             pixels = im.load()
#             x, y = im.size

#             white_pix = 0
#             another_pix = 0

#             for i in range(x):
#                 for j in range(y):
#                     color = pixels[i, j]
#                     flag = True
#                     for q in range(3):
#                         if pixels[i, j][q] == 255:
#                             flag = False
#                     if flag:
#                         white_pix += 1
#                     another_pix += 1
#             print(white_pix)
#             print(another_pix)
#             # 
            
#         return render(request, 'PredictionApp/viewPhotoAnalytics.html', {
#             'archive_note': archive_note,
#             'processed_photos': processed_photos
#         })
#     except Exception as e:
#         return JsonResponse({'success': False})


# def index(request):
#     funda = ['funda','of','web','IT']
#     data = "3214"
#     return render(request, 'PredictionApp/index.html', {'data':data, 'funda':funda})
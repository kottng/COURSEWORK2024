# from django.db import models

# class Plant(models.Model):
#     variety = models.CharField(max_length=100)
    
#     identifier = models.CharField(max_length=100, unique=True)
    
#     description = models.TextField()
    
#     preview_image = models.ImageField(upload_to='plant_previews/')
    
#     planting_date = models.DateField()
    
#     def __str__(self):
#         return self.identifier + " " + self.variety

# class PlantPhoto(models.Model):
#     plant = models.ForeignKey(Plant, related_name='photos', on_delete=models.CASCADE)
    
#     photo = models.ImageField(upload_to='plant_photos/')
    
#     date_taken = models.DateField()
    
    
    
    
    
    
    
from django.contrib.auth.models import User
# from django.db import models

# class Plant(models.Model):
#     user = models.ForeignKey(User, related_name='plants', on_delete=models.CASCADE, null=True, blank=True)
#     variety = models.CharField(max_length=100)
#     identifier = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     preview_image = models.ImageField(upload_to='images')
#     planting_date = models.DateField(null=True, blank=True)
    
#     def __str__(self):
#         return self.identifier  + " " + self.variety

# class PlantPhoto(models.Model):
#     plant = models.ForeignKey(Plant, related_name='photos', on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to='plant_photos/')
#     date_taken = models.DateField()
#     greenhouse_temprature = models.TextField(blank=True)
#     greenhouse_humidity = models.TextField(blank=True)
#     greenhouse_illumination = models.TextField(blank=True)
#     plant_supply_N = models.TextField(blank=True)
#     plant_supply_P = models.TextField(blank=True)
#     plant_supply_K = models.TextField(blank=True)

# class PlantAnalytics(models.Model):
#     plant_photo = models.OneToOneField(PlantPhoto, related_name='analytics', on_delete=models.CASCADE, null=True)
#     disease_degree = models.IntegerField(blank=True)
#     disease_degree_description = models.TextField(blank=True)
#     plant_photo_processed = models.ImageField(blank=True)
    
# class Image(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='images')
#     def __str__(self):
#         return self.title
    
    
    
    
    
    
    
# from django.contrib.auth.models import User
# from django.db import models

# class Plant(models.Model):
#     user = models.ForeignKey(User, related_name='plants', on_delete=models.CASCADE, null=True, blank=True)
#     variety = models.CharField(max_length=100)
#     identifier = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     preview_image = models.ImageField(upload_to='images')
#     planting_date = models.DateField(null=True, blank=True)
    
#     def __str__(self):
#         return self.identifier  + " " + self.variety

# class ArchiveNote(models.Model):
#     plant = models.ForeignKey(Plant, related_name='note', on_delete=models.CASCADE)
#     date_taken = models.DateField()
#     greenhouse_temprature = models.TextField(blank=True)
#     greenhouse_humidity = models.TextField(blank=True)
#     greenhouse_illumination = models.TextField(blank=True)
#     plant_supply_N = models.TextField(blank=True)
#     plant_supply_P = models.TextField(blank=True)
#     plant_supply_K = models.TextField(blank=True)

# class PlantPhoto(models.Model):
#     archiveNote = models.ForeignKey(ArchiveNote, related_name='photo', on_delete=models.CASCADE, null=True)
#     photo = models.ImageField(upload_to='plant_photos/')


# class PlantAnalytics(models.Model):
#     plant_photo = models.ForeignKey(PlantPhoto, related_name='analytics', on_delete=models.CASCADE, null=True)
#     # disease_degree = models.IntegerField(blank=True)
#     # disease_degree_description = models.TextField(blank=True)
#     plant_photo_processed = models.ImageField(blank=True)
    
# # class Image(models.Model):
# #     title = models.CharField(max_length=200)
# #     image = models.ImageField(upload_to='images')
# #     def __str__(self):
# #         return self


from django.db import models
from .yandex_storage import YandexDiskStorage

storage = YandexDiskStorage()

class Plant(models.Model):
    user = models.ForeignKey(User, related_name='plants', on_delete=models.CASCADE, null=True, blank=True)
    variety = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    preview_image = models.ImageField(upload_to='images', storage=storage)
    planting_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.identifier + " " + self.variety

class ArchiveNote(models.Model):
    plant = models.ForeignKey(Plant, related_name='note', on_delete=models.CASCADE)
    date_taken = models.DateField()
    greenhouse_temperature = models.TextField(blank=True)
    greenhouse_humidity = models.TextField(blank=True)
    greenhouse_illumination = models.TextField(blank=True)
    plant_supply_N = models.TextField(blank=True)
    plant_supply_P = models.TextField(blank=True)
    plant_supply_K = models.TextField(blank=True)

class PlantPhoto(models.Model):
    archiveNote = models.ForeignKey(ArchiveNote, related_name='photo', on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='plant_photos/', storage=storage)

class PlantAnalytics(models.Model):
    plant_photo = models.ForeignKey(PlantPhoto, related_name='analytics', on_delete=models.CASCADE, null=True)
    plant_photo_processed = models.ImageField(blank=True, storage=storage)

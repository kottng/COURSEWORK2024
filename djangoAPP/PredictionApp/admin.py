from django.contrib import admin
from .models import Plant
from .models import PlantPhoto
from .models import PlantAnalytics
# Register your models here.
admin.site.register(Plant)
admin.site.register(PlantPhoto)
admin.site.register(PlantAnalytics)
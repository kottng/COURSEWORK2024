from django.urls import path, include
from django.contrib import admin
from . import views

from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from PredictionApp.viewsets.viewset import PlantViewSet
from PredictionApp.viewsets.viewset import ArchiveNoteViewSet
from PredictionApp.viewsets.viewset import PlantPhotoViewSet
from PredictionApp.viewsets.viewset import PlantAnalyticsViewSet

router = DefaultRouter()
router.register(r'Plants', PlantViewSet)
router.register(r'ArchiveNotes', ArchiveNoteViewSet)
router.register(r'PlantPhotos', PlantPhotoViewSet)
router.register(r'PlantAnalytics', PlantAnalyticsViewSet)


urlpatterns = [
    # path('BotanicView/', views.index),
    path('', views.Plants, name="Plants"),
    path('viewPlant/<int:id>/', views.viewPlant, name="viewPlant"),
    path('addPlant/', views.addPlant, name="addPlant"),
    path('delete-plant/<int:plant_id>/', views.delete_plant, name='deletePlant'),
    # path('viewAnalytics/<int:id>/', views.viewAnalytics, name="viewAnalytics"),
    path('viewArchiveNote/<int:id>/', views.viewArchiveNote, name="viewArchiveNote"),
    path('addArchiveNote/<int:id>/', views.addArchiveNote, name="addArchiveNote"),
    path('deleteArchiveNote/<int:id>/', views.deleteArchiveNote, name='deleteArchiveNote'),
    # path('makeAnalytics/<int:id>/', views.makeAnalytics, name='makeAnalytics'),
    path('myProfile/', views.myProfile, name="myProfile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('myProfile', views.myProfile, name="myProfile"),
    path('viewPhotoAnalytics/<int:id>/', views.viewPhotoAnalytics, name="viewPhotoAnalytics"),
    # path('test', views.test, name="test"),
    path('processed-photos/<int:archive_note_id>/', views.get_processed_photos, name='get_processed_photos'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from rest_framework import viewsets
from PredictionApp.models import Plant
from PredictionApp.models import PlantPhoto
from PredictionApp.models import ArchiveNote
from PredictionApp.models import PlantAnalytics
from PredictionApp.serializers.serializers import PlantSerializer
from PredictionApp.serializers.serializers import ArchiveNoteSerializer
from PredictionApp.serializers.serializers import PlantPhotoSerializer
from PredictionApp.serializers.serializers import PlantAnalyticsSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    
class ArchiveNoteViewSet(viewsets.ModelViewSet):
    queryset = ArchiveNote.objects.all()
    serializer_class = ArchiveNoteSerializer

class PlantPhotoViewSet(viewsets.ModelViewSet):
    queryset = PlantPhoto.objects.all()
    serializer_class = PlantPhotoSerializer

class PlantAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = PlantAnalytics.objects.all()
    serializer_class = PlantAnalyticsSerializer

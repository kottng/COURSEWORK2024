from rest_framework import serializers
from PredictionApp.models import Plant
from PredictionApp.models import PlantPhoto
from PredictionApp.models import ArchiveNote
from PredictionApp.models import PlantAnalytics

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'
        
class ArchiveNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveNote
        fields = '__all__'
        
class PlantPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPhoto
        fields = '__all__'
        
class PlantAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantAnalytics
        fields = '__all__'      
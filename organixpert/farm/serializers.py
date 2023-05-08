from rest_framework import serializers

from .models import Farm, Crops

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['farm_owner', 'farm_size', 'farm_location', 'soil_type', 'crop_grown', 'seed_variety', 'soil_nitrogen_level', 'soil_phosphorus_level', 'soil_potassium_level']
        
        
class CropsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crops
        fields = ['crop_type', 'seed_variety', 'nitrogen_requirement', 'phosphorus_requirement', 'potassium_requirement']
        

class UploadSerializer(serializers.FileField):
    file_uploaded = serializers.FileField()
    class Meta:
        fields = ['file_uploaded']
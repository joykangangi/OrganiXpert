from django.db import models
from django.contrib.auth.models import User

class Crops(models.Model):
    crop_type = models.CharField(max_length=50, blank=True)
    seed_variety = models.CharField(max_length=50, blank=True)
    nitrogen_requirement = models.CharField(max_length=50, blank=True)
    phosphorus_requirement = models.CharField(max_length=50, blank=True)
    potassium_requirement = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.seed_variety
    

class Farm(models.Model):
    farm_owner = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_size = models.CharField(max_length=50, blank=True)
    farm_location = models.CharField(max_length=50, blank=True)
    soil_type = models.CharField(max_length=50, blank=True)
    crop_grown = models.CharField(max_length=50, blank=True)
    seed_variety = models.CharField(max_length=50, blank=True)
    soil_nitrogen_level = models.CharField(max_length=50, blank=True)
    soil_phosphorus_level = models.CharField(max_length=50, blank=True)
    soli_potassium_level = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.farm_owner.username
    
    

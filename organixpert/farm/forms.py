from django import forms
from .models import Farm

class FarmDetailRegistrationForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['farm_size', 'farm_location', 'soil_type', 'crop_grown', 'seed_variety']
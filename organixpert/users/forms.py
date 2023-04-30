from allauth.account.forms import SignupForm
from django import forms
from .models import Profile

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    
    class Meta:
        model = Profile
        fields = ('national_id')
        
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        user.profile.national_id = self.cleaned_data['national_id']
        user.profile.save()
from django.urls import path
from .views import upload, get_recommendation, farm_details_registration

urlpatterns = [
    path('/farm-detail-registration', farm_details_registration, name='farm_details_registration'),
    path('/upload', upload, name='upload'),
    path('/recommend', get_recommendation, name='recommend'),
]

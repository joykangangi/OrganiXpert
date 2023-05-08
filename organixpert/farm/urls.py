from django.urls import path, include
from .views import upload, get_recommendation, farm_details_registration, SoilTestReportViewSet
from rest_framework import routers

urlpatterns = [
    path('farm/farm-detail-registration', farm_details_registration, name='farm_details_registration'),
    path('farm/upload', upload, name='upload'),
    path('farm/recommend', get_recommendation, name='recommend'),
]

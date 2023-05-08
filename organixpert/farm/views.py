from rest_framework.decorators import api_view, permission_classes, parser_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, parsers
from rest_framework.viewsets import ViewSet
from .serializers import FarmSerializer, UploadSerializer

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from .models import Farm, Crops
from .forms import FarmDetailRegistrationForm
import os
import pickle
from .preprocessing import preprocess_before_inference
from .number_of_bags import determine_number_of_bags
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(method='post', request_body=FarmSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def farm_details_registration(request):
    try:
        farm = Farm.objects.get(farm_owner=request.user)
        content = {'message': 'You have already registered your farm details.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Farm.DoesNotExist:
        data = request.data
        farm_details = Farm.objects.create(
            farm_owner=request.user,
            farm_size=data['farm_size'],
            farm_location=data['farm_location'],
            soil_type=data['soil_type'],
            crop_grown=data['crop_grown'],
            seed_variety=data['seed_variety'],
            soil_nitrogen_level=data['soil_nitrogen_level'],
            soil_phosphorus_level=data['soil_phosphorus_level']
        )
        serializer = FarmSerializer(farm_details, many=False)
        return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_description="Upload soil test report",
    operation_id="upload_soil_test_report",
    request_body=openapi.Schema(
        type='object',
        properties={
            'pdf_file': openapi.Schema(type='file'),
        }
    ),
    responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'},
    tags=['farm'],
    manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Authorization Token", type=openapi.TYPE_STRING)],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload(request):
    user = request.user
    uploaded_file = request.FILES.get('pdf_file')
    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    pdf_file_url = fs.url(filename)
    reader = PdfReader(pdf_file_url)
    page = reader.pages[0]
    text = page.extract_text()
    lines = text.splitlines()
    for i, v in enumerate(lines):
        if v == 'Nitrogen':
            nitrogen = lines[i+1]
        elif v == 'Phosphorus':
            phosphorus = lines[i+1]
        elif v == 'Potassium':
            potassium = lines[i+1]
        else:
            pass
    # convert nitrogen, phosphorus, potassium ppm values to kg/acre values
    # 2.24 is the conversion factor from ppm to kg/ha
    # 0.4047 is the conversion factor from kg/ha to kg/acre
    nitrogen = str(round(float(nitrogen) * 2.24 * 0.4047, 2))
    phosphorus = str(round(float(phosphorus) * 2.24 * 0.4047, 2))
    potassium = str(round(float(potassium) * 2.24 * 0.4047, 2))
    farm = Farm.objects.get(farm_owner=user)
    farm.update(soil_nitrogen_level=nitrogen,
                soil_phosphorus_level=phosphorus, soil_potassium_level=potassium)
    return Response({'message': 'Soil test results uploaded successfully.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation(request):
    user = request.user
    farm = Farm.objects.get(farm_owner=user)
    nitrogen = farm.soil_nitrogen_level
    phosphorus = farm.soil_phosphorus_level
    potassium = farm.soil_potassium_level
    variety = farm.seed_variety
    soil_content = [nitrogen, phosphorus, potassium]
    crop = farm.crop_grown
    soil_type = farm.soil_type
    crop_requirements = Crops.objects.filter(crop_type=crop, seed_variety=variety).first()
    nitrogen_required = None
    phosphorus_required = None
    potassium_required = None
    if crop_requirements:
        nitrogen_required = crop_requirements.nitrogen_requirement
        phosphorus_required = crop_requirements.phosphorus_requirement
        potassium_required = crop_requirements.potassium_requirement
    else:
        print('No crop requirements found')
    nutrient_requirements = [nitrogen_required, phosphorus_required, potassium_required]
    # prepare the data for inferencing
    data = [[soil_type, crop, nitrogen, potassium, phosphorus]]
    data = preprocess_before_inference(data)
    # load the model from disk using pickle module
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ml_dev_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, 'ML_Development'))
    model_path = os.path.join(ml_dev_dir, 'Models')
    if os.path.exists(model_path):
        os.chdir(model_path)
        print('Changed directory to {}'.format(model_path))
    else:
        print('Directory {} does not exist'.format(model_path))
    with open('Organic_Fertilizer_Recommender.pkl', 'rb') as file:
        model = pickle.load(file)
    # make predictions
    print(data)
    prediction = model.predict(data)
    organic_fertilizers = ['Safi Biochar',
                           'Safi Sarvi Planting Fertilizer', 'Safi Sarvi Topper']
    predicted_fertilizer = organic_fertilizers[prediction[0]]
    print(predicted_fertilizer)
    bags = determine_number_of_bags(nutrient_requirements, soil_content, predicted_fertilizer)
    return Response({'fertilizer': predicted_fertilizer, 'bags': bags})


class SoilTestReportViewSet(ViewSet):
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [IsAuthenticated]
    serializer_class = UploadSerializer
    
    @action(detail=False, methods=['post'], url_path='farm/upload')
    def upload(self, request):
        user = request.user
        uploaded_file = request.FILES.get('pdf_file')
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        pdf_file_url = fs.url(filename)
        reader = PdfReader(pdf_file_url)
        page = reader.pages[0]
        text = page.extract_text()
        lines = text.splitlines()
        nitrogen = None
        phosphorus = None
        potassium = None
        for i, v in enumerate(lines):
            if v == 'Nitrogen':
                nitrogen = lines[i+1]
            elif v == 'Phosphorus':
                phosphorus = lines[i+1]
            elif v == 'Potassium':
                potassium = lines[i+1]
            else:
                pass
        if not all([nitrogen, phosphorus, potassium]):
            return Response({'message': 'Invalid soil test report.'}, status=status.HTTP_400_BAD_REQUEST)
        # convert nitrogen, phosphorus, potassium ppm values to kg/acre values
        # 2.24 is the conversion factor from ppm to kg/ha
        # 0.4047 is the conversion factor from kg/ha to kg/acre
        nitrogen = str(round(float(nitrogen) * 2.24 * 0.4047, 2))
        phosphorus = str(round(float(phosphorus) * 2.24 * 0.4047, 2))
        potassium = str(round(float(potassium) * 2.24 * 0.4047, 2))
        farm = Farm.objects.get(farm_owner=user)
        farm.soil_nitrogen_level = nitrogen
        farm.soil_phosphorus_level = phosphorus
        farm.soli_potassium_level = potassium
        farm.save()
        return Response({'message': 'Soil test results uploaded successfully.'})
    
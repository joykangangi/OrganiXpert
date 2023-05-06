from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from .models import Farm, Crops
from .forms import FarmDetailRegistrationForm
import os, pickle
from .preprocessing import preprocess_before_inference
from .number_of_bags import determine_number_of_bags

@login_required
def farm_details_registration(request):
    try:
        farm = Farm.objects.get(farm_owner=request.user)
        return redirect('index')
    except Farm.DoesNotExist:
        if request.method == 'POST':
            form = FarmDetailRegistrationForm(request.POST)
            if form.is_valid():
                farm = form.save(commit=False)
                farm.farm_owner = request.user
                farm.save()
                return redirect('index')
        else:
            form = FarmDetailRegistrationForm()
            return render(request, 'farm_details_registration.html', {'form': form})

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        uploaded_file = request.FILES['pdf_file']
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
        farm = Farm.objects.get(farm_owner=request.user)
        farm.update(soil_nitrogen_level=nitrogen, soil_phosphorus_level=phosphorus, soli_potassium_level=potassium)
        return render(request, 'upload_success.html', {'pdf_url': pdf_file_url})
    return render(request, 'upload.html')

@login_required
def get_recommendation(request):
    user = request.user
    farm = Farm.objects.get(farm_owner=user)
    nitrogen = farm.soil_nitrogen_level
    phosphorus = farm.soil_phosphorus_level
    potassium = farm.soli_potassium_level
    variety = farm.seed_variety
    soil_content = [nitrogen, phosphorus, potassium]
    crop = farm.crop_grown
    soil_type = farm.soil_type
    crop_requirements = Crops.objects.get(crop_type=crop).filter(seed_variety=variety)
    nitrogen_required = crop_requirements.nitrogen_requirement
    phosphorus_required = crop_requirements.phosphorus_requirement
    potassium_required = crop_requirements.potassium_requirement
    nutrient_requirements = [nitrogen_required, phosphorus_required, potassium_required]
    # prepare the data for inferencing
    data = [[soil_type, crop, nitrogen, potassium, phosphorus]]
    data = preprocess_before_inference(data)
    # load the model from disk using pickle module
    model_path = os.path.abspath('../../ML_Development/Models')
    os.chdir(model_path)
    with open('Organic_Fertilizer_Recommender.pkl', 'rb') as file:
        model = pickle.load(file)
    # make predictions
    prediction = model.predict(data)
    organic_fertilizers = ['Safi Biochar', 'Safi Sarvi Planting Fertilizer', 'Safi Sarvi Topper']
    predicted_fertilizer = organic_fertilizers[prediction]
    bags = determine_number_of_bags(nutrient_requirements, soil_content, predicted_fertilizer)
    return render(request, 'recommendation.html', {'fertilizer': predicted_fertilizer, 'bags': bags})
    

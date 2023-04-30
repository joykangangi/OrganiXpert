from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from .models import Farm, Crops
from .forms import FarmDetailRegistrationForm

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
        Farm.objects.create(farm_owner=request.user, soil_nitrogen_level=nitrogen, soil_phosphorus_level=phosphorus, soli_potassium_level=potassium)
        return render(request, 'upload_success.html', {'pdf_url': pdf_file_url})
    return render(request, 'upload.html')

@login_required
def get_recommendation(request):
    user = request.user
    farm = Farm.objects.get(farm_owner=user)
    nitrogen = farm.soil_nitrogen_level
    phosphorus = farm.soil_phosphorus_level
    potassium = farm.soli_potassium_level
    crop = farm.crop_grown
    soil_type = farm.soil_type
    crop_requirements = Crops.objects.get(crop_type=crop).filter(seed_variety=farm.seed_variety)
    # inference machine learning model
    return render(request, 'recommendation.html')
    

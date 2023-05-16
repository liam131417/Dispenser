from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MedicineDetail
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def addMedicine(request):
    if request.method == 'POST':
        name = request.POST.get('drug_name')
        condition = request.POST.get('medical_condition')
        alcohol = request.POST.get('alcohol')
        pregnant = request.POST.get('pregnancy_category')
        rating = request.POST.get('rating')
        rx_otc = request.POST.get('rx_otc')
        side_effects = request.POST.get('side_effects')
        if name is None or condition is None or alcohol is None or rating is None or rx_otc is None or side_effects is None:
            return JsonResponse({'error':"Invalid response from null name"})
        md = MedicineDetail.objects.create(name = name,condition = condition,alcohol = alcohol,pregnant = pregnant,rating = rating,rx_otc = rx_otc,side_effects = side_effects)
        data = {
            "name" : md.name,
            "condition":md.condition,
            "alcohol":md.alcohol,
            "pregnant":md.pregnant,
            "rating":md.rating,
            "rx_otc":md.rx_otc,
            "side_effects":md.side_effects
        }
        return JsonResponse(data)
    else: 
        return JsonResponse({'error':"Invalid response from not post"})


def get_medicine(request,name):
    try:
        md = MedicineDetail.objects.get(pk=name.lower())
        data = {'name': md.name, 'condition': md.condition, 'alcohol': md.alcohol, 'pregnant': md.pregnant, 'rating': md.rating, 'rx_otc': md.rx_otc, 'side_effects': md.side_effects}
        return data
    except MedicineDetail.DoesNotExist:
        return JsonResponse({'error':"Name does not exist"})

def check_medicine(request, input_name, input_condition, input_alcohol, input_pregnant):
    input_name = input_name.lower()
    input_condition = input_condition.lower()
    input_alcohol = input_alcohol.upper()
    input_pregnant = input_pregnant.upper()

    try:
        md = MedicineDetail.objects.get(pk=input_name.lower())
        data = {'name': md.name, 'condition': md.condition, 'alcohol': md.alcohol, 'pregnant': md.pregnant, 'rating': md.rating, 'rx_otc': md.rx_otc, 'side_effects': md.side_effects}

        message = ''
        ap_msg = check_alcohol_pregnancy(input_alcohol, input_pregnant, data)

        if data['condition'] == input_condition:
            message = ap_msg
            return message, data
        else:
            message = 'This medicine mainly used for ' + data['condition'] + '. ' + ap_msg
            return message, recommend(input_condition, input_alcohol, input_pregnant)
        
    except MedicineDetail.DoesNotExist:
        return JsonResponse({'error':"Name does not exist"})

def recommend(input_condition, input_alcohol, input_pregnant):
    input_condition = input_condition.lower()
    input_alcohol = input_alcohol.upper()
    input_pregnant = input_pregnant.upper()
    # search for the records based on medicine_name and medical_condition
    matched_records = MedicineDetail.objects.filter(condition__icontains=input_condition).order_by('-rating')[:3]
    if input_alcohol == 'Y':
        matched_records = MedicineDetail.objects.filter(condition__icontains=input_condition, alcohol='S').order_by('-rating')[:3]

    if input_pregnant == 'Y':
        matched_records = MedicineDetail.objects.filter(condition__icontains=input_condition, pregnant__in=['A', 'B']).order_by('-rating')[:3]

    if input_alcohol == 'Y' and input_pregnant == 'Y':
        matched_records = MedicineDetail.objects.filter(condition__icontains=input_condition, alcohol='S', pregnant__in=['A', 'B']).order_by('-rating')[:3]
        
    if (len(matched_records) > 0):
        # convert matched records to a list of dictionaries
        data = list(matched_records.values())
        # return the records as a JSON response
        return data
    else:
        return JsonResponse({'error':"No records found"})
    
def check_alcohol_pregnancy(input_alcohol, input_pregnant, data):
    message = ''

    # Check alcohol
    if input_alcohol == 'Y' and data['alcohol'] == 'D':
        message += 'This patient drinks alcohol but the medicine is not safe to consume with alcohol. '

    # Check pregnancy
    if input_pregnant == 'Y' and data['pregnant'] in {'C', 'D', 'X', 'N'}:
        message += 'This patient is pregnant but the medicine is not suitable for pregnant woman. '

    return message
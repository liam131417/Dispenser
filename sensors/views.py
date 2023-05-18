from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import HumiditySensor
from .models import MotionSensor
from .models import UltrasonicSensor
from .models import MedicalDispensor,DispenseRecord
import json

from django.utils import timezone
from datetime import datetime, timedelta, date
import random
from django.db.models import Count
from django.db.models.functions import TruncMonth,TruncWeek


from sensors.models import DispenseRecord


@csrf_exempt
def add_tempAndHumid(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body.get('id')
        temp = body.get('temp')
        humidity = body.get('humidity')
        if id is None or temp is None or humidity is None:
            return JsonResponse({'error':"Invalid responseif"})
        temphumid = HumiditySensor.objects.create(id=id,temperature=temp,humidity=humidity)
        data = {
            "id" : temphumid.id,
            "temperature":temphumid.temperature,
            "humidity":temphumid.humidity
        }
        return JsonResponse(data)
    else: 
        return JsonResponse({'error':"Invalid responseelse"})
    
@csrf_exempt
def add_tempAndHumidCreatedAt(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        id = body.get('id')
        temp = body.get('temp')
        humidity = body.get('humidity')
        created_a = body.get('created_at')
        if id is None or temp is None or humidity is None:
            return JsonResponse({'error':"Invalid responseif"})
        temphumid = HumiditySensor.objects.create(id=id,temperature=temp,humidity=humidity,created_at=created_a)
        data = {
            "id" : temphumid.id,
            "temperature":temphumid.temperature,
            "humidity":temphumid.humidity
        }
        return JsonResponse(data)
    else: 
        return JsonResponse({'error':"Invalid responseelse"})

@csrf_exempt
def add_dist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        distance = data.get('distance')
        if id is None or distance is None:
            return JsonResponse({'error':"Invalid response"})
        dist = UltrasonicSensor.objects.create(id=id, distance=distance)
        response_data = {
            "id" : dist.id,
            "distance": dist.distance
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error':"Invalid response"})
@csrf_exempt
def add_motion(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        motion = request.POST.get('motion')
        if id is None or motion is None:
            return JsonResponse({'error':"Invalid response"})
        motionDetect = MotionSensor.objects.create(id=id,motion=motion)
        data = {
            "id" : motionDetect.id,
            "motion":motionDetect.motion
            }
        return JsonResponse(data)
    else: 
        return JsonResponse({'error':"Invalid response"})

# @csrf_exempt
# def add_dist(request):
#     if request.method == 'POST':
#         id = request.POST.get('id')
#         distance = request.POST.get('distance')
#         if id is None or distance is None:
#             return JsonResponse({'error':"Invalid response","id":id})
#         dist = UltrasonicSensor.objects.create(id=id,distance=distance)
#         data = {
#             "id" : dist.id,
#             "distance":dist.distance
#         }
#         return JsonResponse(data)
#     else: 
#         return JsonResponse({'error':"Invalid response"})



@csrf_exempt
def addDispesnsor(request):
    if request.method == 'POST':
        id = request.POST.get('id',None)
        isDispensing = request.POST.get('isDispensing',False)
        medicine = request.POST.get('humidity',None)
        if id is None or medicine is None:
            return JsonResponse({'error':"Invalid responseif"})
        md = MedicalDispensor.objects.create(id=id,isDispensing=isDispensing,medicine= medicine)
        data = {
            "id" : md.id,
            "isDeispensing":md.isDispensing,
            "medicine":md.medicine
        }
        return JsonResponse(data)
    else: 
        return JsonResponse({'error':"Invalid responseelse"})

# @csrf_exempt
# def addMedicine(request):
#     if request.method == 'POST':
#         name = request.POST.get('name',None)
#         condition = request.POST.get('condition',"")
#         alcohol = request.POST.get('humidity',False)
#         pregnant = request.POST.get('pregnant','')
#         if name is None:
#             return JsonResponse({'error':"Invalid response"})
#         md = MedicineDetail.objects.create(name = name,condition = condition,alcohol = alcohol,pregnant = pregnant)
#         data = {
#             "name" : md.name,
#             "condition":md.condition,
#             "alcohol":md.alcohol,
#             "pregnant":md.pregnant
#         }
#         return JsonResponse(data)
#     else: 
#         return JsonResponse({'error':"Invalid response"})

def get_temphumid(request, id):
    try:
        temphumid = HumiditySensor.objects.get(pk=id)
        data = {
            'id' : temphumid.id,
            'temperature':temphumid.temperature,
            'humidity':temphumid.humidity
        }
        return JsonResponse(data,safe=False)
    except HumiditySensor.DoesNotExist:
        return JsonResponse({'error':"ID does not exist"})


def get_distance(request, id):
    try:
        distance = UltrasonicSensor.objects.get(pk=id)
        data = {
            'id' : distance.id,
            'distance':distance.distance
        }
        return JsonResponse(data,safe=False)
    except UltrasonicSensor.DoesNotExist:
        return JsonResponse({'error':"ID does not exist"})

def get_motion(request,id):
    try:
        motion = MotionSensor.objects.get(pk=id)
        data = {
            'id' : motion.id,
            'motion':motion.motion
        }
        return JsonResponse(data,safe=False)
    except MotionSensor.DoesNotExist:
        return JsonResponse({'error':"ID does not exist"})

def get_disp(request,id):
    try:
        disp = MedicalDispensor.objects.get(pk=id)
        data = {
            'isDispensing':disp.isDispensing,
            'medicine':disp.medicine,
            'ultraId':disp.ultraId,
            'tempId':disp.tempId
        }
        return JsonResponse(data,safe=False)
    except MedicalDispensor.DoesNotExist:
        return JsonResponse({'error':"ID does not exist"})
@csrf_exempt
def incrementDist(request,id):
    try:
        obj = MedicalDispensor.objects.get(pk=id)
        obj.ultraId += 1
        obj.save()
        return JsonResponse({'success': True})
    except MedicalDispensor.DoesNotExist:
        return JsonResponse({'error': 'Object not found'})
@csrf_exempt
def incrementTemp(request,id):
    try:
        obj = MedicalDispensor.objects.get(pk=id)
        obj.tempId += 1
        obj.save()
        return JsonResponse({'success': True})
    except MedicalDispensor.DoesNotExist:
        return JsonResponse({'error': 'Object not found'})
@csrf_exempt
def isDispensing(request,id):
    try:
        obj = MedicalDispensor.objects.get(pk=id)
        obj.isDispensing = True
        obj.save()
        return JsonResponse({'success': True})
    except MedicalDispensor.DoesNotExist:
        return JsonResponse({'error': 'Object not found'})
@csrf_exempt
def isNotDispensing(request,id):
    try:
        obj = MedicalDispensor.objects.get(pk=id)
        obj.isDispensing = False
        obj.save()
        return JsonResponse({'success': True})
    except MedicalDispensor.DoesNotExist:
        return JsonResponse({'error': 'Object not found'})

@csrf_exempt
def motionDetected(request,id):
    try:
        obj = MotionSensor.objects.get(pk=id)
        obj.motion = 1
        obj.save()
        return JsonResponse({'success': True})
    except MotionSensor.DoesNotExist:
        return JsonResponse({'error': 'Object not found'})

@csrf_exempt
def motionNotDetected(request,id):
    try:
        obj = MotionSensor.objects.get(pk=id)
        obj.motion = 0
        obj.save()
        return JsonResponse({'success': True})
    except MotionSensor.DoesNotExist:
        return JsonResponse({'error': 'Object not found'})


def motion(request):
    if request.method == 'GET':
        motion = MotionSensor.objects.all()
        data = [{
            'id' : m.id,
            'motion':m.motion
        }for m in motion]
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'error':"Error"})

def temphumid(request):
    if request.method == 'GET':
        temphumid = HumiditySensor.objects.all()
        data = [{
            'id' : t.id,
            'temperature':t.temperature,
            'humidity':t.humidity
        }for t in temphumid]
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'error':"ID does not exist"})

def distance(request):
    if request.method == 'GET':
        distance = UltrasonicSensor.objects.all()
        data = [{
            'id' : d.id,
            'distance':d.distance
        }for d in distance]
        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'error':"ID does not exist"})

@csrf_exempt   
def getSeed(request):
    for i in range(365):
            y=timezone.now()-timedelta(days=i)
            HumiditySensor.objects.create(
                id = i,
                temperature=random.uniform(26, 32),
                created_at=y,
                humidity =random.uniform(40,85)
            )
            UltrasonicSensor.objects.create(
                id = i,
                distance = random.uniform(0,22),
                created_at = y
            )
    return JsonResponse({'success':'success'})

@csrf_exempt   
def seed_data(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=365)

    dispId_choices = [1, 2, 3]
    medicine_choices = ['paracetamol', 'aspirin', 'ibuprofen']

    for day in range((today - start_date).days):
        date = start_date + timedelta(days=day)

        # Generate a random number of entries for the day
        num_entries = random.randint(5, 15)

        for _ in range(num_entries):
            # Randomly select dispId, medicine, quantity, and set pillQuantity to 10
            dispId = random.choice(dispId_choices)
            medicine = random.choice(medicine_choices)
            quantity = random.randint(1, 5)
            pillQuantity = 10

            # Create the DispenseRecord entry
            DispenseRecord.objects.create(
                created_at=date,
                dispId=dispId,
                medicine=medicine,
                quantity=quantity,
                pillQuantity=pillQuantity
            )

    return JsonResponse({'message': 'Data seeded successfully.'})

def entries_by_month():
    entries = DispenseRecord.objects\
        .annotate(month=TruncMonth('created_at'))\
        .values('month')\
        .annotate(count=Count('id'))\
        .order_by('month')
    
    monthly_counts = [0] * 12
    
    for entry in entries:
        month = entry['month'].month
        count = entry['count']
        monthly_counts[month - 1] = count
    
    return monthly_counts


def entries_by_last_12_weeks():
    # Calculate the date range for the last 12 weeks
    today = date.today()
    start_date = today - timedelta(weeks=11)  # Start from 11 weeks ago
    end_date = today + timedelta(days=1)  # End today (inclusive)

    entries = DispenseRecord.objects\
        .filter(created_at__date__range=(start_date, end_date))\
        .annotate(week=TruncWeek('created_at'))\
        .values('week')\
        .annotate(count=Count('id'))\
        .order_by('week')

    weekly_counts = [0] * 12

    for entry in entries:
        week_start = entry['week']
        week_end = week_start + timedelta(weeks=1) - timedelta(days=1)
        count = entry['count']

        # Find the index of the week within the last 12 weeks range
        index = (week_start.date() - start_date).days // 7
        weekly_counts[index] = count

    return weekly_counts
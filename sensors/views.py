from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import HumiditySensor
from .models import MotionSensor
from .models import UltrasonicSensor
from .models import MedicalDispensor
import json

from django.utils import timezone
from datetime import timedelta
import random



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

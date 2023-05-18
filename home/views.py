# home/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import DispenseForm, ConfigForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from sensors.models import HumiditySensor
from sensors.models import MotionSensor
from sensors.models import UltrasonicSensor
from sensors.models import MedicalDispensor, DispenseRecord
from datetime import date, timedelta
from .analysis import predictTemp
from .analysis import predictHumidity
from sensors.views import isDispensing
from medicine.views import check_medicine, recommend, get_medicine
from medicine.models import MedicineDetail
from django.contrib import messages
from django.utils import timezone


temp_threshold = 20.0
humid_threshold = 20.0

def home(request):
    return render(request, 'home/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})

def get_temp_humid_dist(request):
    try:
        md = MedicalDispensor.objects.get(pk=1)
        temp = HumiditySensor.objects.get(pk = md.tempId)
        dist = UltrasonicSensor.objects.get(pk = md.ultraId)
        return temp.temperature,temp.humidity,dist.distance
    except HumiditySensor.DoesNotExist or UltrasonicSensor.DoesNotExist:
        for i in range(1, md.tempId + 1):
                try:
                    temp = HumiditySensor.objects.get(pk=md.tempId - i)
                    break
                except HumiditySensor.DoesNotExist:
                    continue
            
        for j in range(1, md.ultraId + 1):
            try:
                dist = UltrasonicSensor.objects.get(pk=md.ultraId - j)
                break
            except UltrasonicSensor.DoesNotExist:
                continue
                    
        return temp.temperature, temp.humidity, dist.distance


def get_forecast():
    today = date.today()
    # Calculate the date for next week
    next_week = today + timedelta(weeks=1)
    # Extract the year, month, and day from the next week date
    year = next_week.year
    month = next_week.month
    day = next_week.day
    return predictTemp(year,month,day),predictHumidity(year,month,day)

@login_required
def dashboard(request):
    temp_data = []
    hum_data = []
    temp_week_data = []
    hum_week_data = []
    for i in range(0,12):
        temp_month = 0
        hum_month = 0
        for j in range(30):
            data = HumiditySensor.objects.get(pk = i+j+1)
            temp_month += float(data.temperature)
            hum_month += float(data.humidity)
        avg_temp = temp_month/30
        avg_hum = hum_month/30
        temp_data.append(avg_temp)
        hum_data.append(avg_hum)
        temp_week = 0
        hum_week = 0
        for j in range(7):
            data = HumiditySensor.objects.get(pk = 365-i-j)
            temp_week += float(data.temperature)
            hum_week += float(data.humidity)
        temp_week_data.append(temp_week/7)
        hum_week_data.append(hum_week/7)
    temp,humid,dist = get_temp_humid_dist(request=request)
    stock = "{dist:.2f}".format(dist=(100-(int(round(float(dist)))/22)*100))
    predTemp,predHum = get_forecast()
    context = {'temp':"{temp:.2f}".format(temp=float(temp)),'humid':"{humid:.2f}".format(humid=float(humid)),'dist':stock,'fTemp':"{pred:.2f}".format(pred=predTemp[0]),
               'fHum':"{pred:.2f}".format(pred=predHum[0]),
               'temp_data':temp_data,
               'hum_data':hum_data,
               'temp_week_data':temp_week_data,
               'hum_week_data':hum_week_data}
    if float(temp) > temp_threshold:
        messages.add_message(request, messages.SUCCESS, 'Temperature exceeds the threshold(' + str(temp_threshold) + ').')
    if float(humid) > humid_threshold:
        messages.add_message(request, messages.SUCCESS, 'Humidity exceeds the threshold(' + str(humid_threshold) + ').')
    return render(request, 'home/dashboard.html',context)

@login_required
def dispense(request):
    form = DispenseForm()
    obj1 = MedicalDispensor.objects.get(pk=1)
    obj2 = MedicalDispensor.objects.get(pk=2)
    obj3 = MedicalDispensor.objects.get(pk=3)
    setup_message = ''
    # Check if dispenser is setup
    if len(obj1.medicine) == 0:
        setup_message = 'Dispenser A is not setup'
        messages.add_message(request, messages.WARNING, setup_message)
        return render(request, 'home/dispense.html', {'form': form})
    if len(obj2.medicine) == 0:
        setup_message = 'Dispenser B is not setup'
        messages.add_message(request, messages.WARNING, setup_message)
        return render(request, 'home/dispense.html', {'form': form})
    if len(obj3.medicine) == 0:
        setup_message = 'Dispenser C is not setup'
        messages.add_message(request, messages.WARNING, setup_message)
        return render(request, 'home/dispense.html', {'form': form})
    
    context = {
        'dispenser1_name': obj1.medicine.capitalize(),
        'dispenser1_quantity': obj1.quantity,
        'dispenser2_name': obj2.medicine.capitalize(),
        'dispenser2_quantity': obj2.quantity,
        'dispenser3_name': obj3.medicine.capitalize(),
        'dispenser3_quantity': obj3.quantity,
    }
    
    if request.method == 'POST':
        form = DispenseForm(request.POST)
        button_clicked = request.POST.get('button')
        # Handle button click logic here
        if button_clicked == 'dispenserA':
            obj = MedicalDispensor.objects.get(pk=1)
            med_name = obj.medicine
            md = MedicineDetail.objects.get(pk=med_name)
            current_obj = {'name': md.name, 'condition': md.condition, 'alcohol': md.alcohol, 'pregnant': md.pregnant, 'rating': md.rating, 'rx_otc': md.rx_otc, 'side_effects': md.side_effects}
            
            if form.is_valid(): 
                preg_input = form.cleaned_data['pregnancy']
                alcohol_input = form.cleaned_data['alcohol']
                recommendation = form.cleaned_data['recommendation']
                quanty = form.cleaned_data['quantity']
                isDispensing(request, 1)
                createdAt = timezone.now()
                medicine = med_name
                dispId = 1
                quantity = quanty
                DispenseRecord.objects.create(created_at=createdAt,dispId = dispId, medicine=medicine,quantity = quantity)

                preg = 'Y' if preg_input else 'N'
                alcohol = 'Y' if alcohol_input else 'N'
                
                condition = current_obj['condition']
                message, return_obj = check_medicine(request, med_name, condition, preg, alcohol)
                # Check alcohol
                alcohol_msg = 'Positive. This medicine is safe for alcoholic person. '
                if alcohol == 'Y' and return_obj['alcohol'] == 'D':
                    alcohol_msg = 'Negative. This medicine is unsafe for alcoholic person. '
                # Check pregnancy
                preg_msg = 'Positive. This medicine is safe for pregnant woman. '
                if preg == 'Y' and return_obj['pregnant'] in {'C', 'D', 'X', 'N'}:
                    preg_msg = 'Negative. This medicine is unsafe for pregnant woman. '
                # Side effect
                side_effects_msg = return_obj['side_effects']
                # OTC
                rx_otc = return_obj['rx_otc']
                rx_otc_msg = 'Prescription needed for this medicine'
                if 'otc' in rx_otc:
                    rx_otc_msg = 'Available over the counter'

                messages.success(request, 'Drug name: ' + med_name)
                messages.success(request, 'Medical Condition: ' + condition)
                if alcohol_input:
                    messages.success(request, 'Alcohol: ' + alcohol_msg)
                if preg_input:
                    messages.success(request, 'Pregnancy: ' + preg_msg)
                messages.success(request, 'Side effects: ' + side_effects_msg)
                messages.success(request, 'Rx/OTC: ' + rx_otc_msg)

                if recommendation:
                    return_objs = recommend(condition, alcohol, preg)
                    for medicine in return_objs:
                        messages.success(request, ' ')
                        current_obj = medicine
                        condition = current_obj['condition']
                        med_name = current_obj['name']
                        message, return_obj = check_medicine(request, med_name, condition, preg, alcohol)
                        
                        side_effects_msg = return_obj['side_effects']
                        rx_otc = return_obj['rx_otc']
                        rx_otc_msg = 'Prescription needed for this medicine'
                        if 'otc' in rx_otc:
                            rx_otc_msg = 'Available over the counter'

                        messages.success(request, 'Drug name: ' + med_name)
                        messages.success(request, 'Medical Condition: ' + condition)
                        messages.success(request, 'Side effects: ' + side_effects_msg)
                        messages.success(request, 'Rx/OTC: ' + rx_otc_msg)
                        
        elif button_clicked == "dispenserB":
            obj = MedicalDispensor.objects.get(pk=2)
            med_name = obj.medicine
            md = MedicineDetail.objects.get(pk=med_name)
            current_obj = {'name': md.name, 'condition': md.condition, 'alcohol': md.alcohol, 'pregnant': md.pregnant, 'rating': md.rating, 'rx_otc': md.rx_otc, 'side_effects': md.side_effects}
            
            if form.is_valid(): 
                preg_input = form.cleaned_data['pregnancy']
                alcohol_input = form.cleaned_data['alcohol']
                recommendation = form.cleaned_data['recommendation']
                quanty = form.cleaned_data['quantity']

                isDispensing(request, 1)
                createdAt = timezone.now()
                medicine = med_name
                dispId = 2
                quantity = quanty
                DispenseRecord.objects.create(created_at=createdAt,dispId = dispId, medicine=medicine,quantity = quantity)

                preg = 'Y' if preg_input else 'N'
                alcohol = 'Y' if alcohol_input else 'N'
                
                condition = current_obj['condition']
                message, return_obj = check_medicine(request, med_name, condition, preg, alcohol)
                # Check alcohol
                alcohol_msg = 'Positive. This medicine is safe for alcoholic person. '
                if alcohol == 'Y' and return_obj['alcohol'] == 'D':
                    alcohol_msg = 'Negative. This medicine is unsafe for alcoholic person. '
                # Check pregnancy
                preg_msg = 'Positive. This medicine is safe for pregnant woman. '
                if preg == 'Y' and return_obj['pregnant'] in {'C', 'D', 'X', 'N'}:
                    preg_msg = 'Negative. This medicine is unsafe for pregnant woman. '
                # Side effect
                side_effects_msg = return_obj['side_effects']
                # OTC
                rx_otc = return_obj['rx_otc']
                rx_otc_msg = 'Prescription needed for this medicine'
                if 'otc' in rx_otc:
                    rx_otc_msg = 'Available over the counter'

                messages.success(request, 'Drug name: ' + med_name)
                messages.success(request, 'Medical Condition: ' + condition)
                if alcohol_input:
                    messages.success(request, 'Alcohol: ' + alcohol_msg)
                if preg_input:
                    messages.success(request, 'Pregnancy: ' + preg_msg)
                messages.success(request, 'Side effects: ' + side_effects_msg)
                messages.success(request, 'Rx/OTC: ' + rx_otc_msg)

                if recommendation:
                    return_objs = recommend(condition, alcohol, preg)
                    for medicine in return_objs:
                        messages.success(request, ' ')
                        current_obj = medicine
                        condition = current_obj['condition']
                        med_name = current_obj['name']
                        message, return_obj = check_medicine(request, med_name, condition, preg, alcohol)
                        
                        side_effects_msg = return_obj['side_effects']
                        rx_otc = return_obj['rx_otc']
                        rx_otc_msg = 'Prescription needed for this medicine'
                        if 'otc' in rx_otc:
                            rx_otc_msg = 'Available over the counter'

                        messages.success(request, 'Drug name: ' + med_name)
                        messages.success(request, 'Medical Condition: ' + condition)
                        messages.success(request, 'Side effects: ' + side_effects_msg)
                        messages.success(request, 'Rx/OTC: ' + rx_otc_msg)

        elif button_clicked == "dispenserC":
            obj = MedicalDispensor.objects.get(pk=3)
            med_name = obj.medicine
            md = MedicineDetail.objects.get(pk=med_name)
            current_obj = {'name': md.name, 'condition': md.condition, 'alcohol': md.alcohol, 'pregnant': md.pregnant, 'rating': md.rating, 'rx_otc': md.rx_otc, 'side_effects': md.side_effects}
            
            if form.is_valid(): 
                preg_input = form.cleaned_data['pregnancy']
                alcohol_input = form.cleaned_data['alcohol']
                recommendation = form.cleaned_data['recommendation']
                isDispensing(request, 1)
                createdAt = timezone.now()
                medicine = med_name
                dispId = 3
                quantity = quanty
                DispenseRecord.objects.create(created_at=createdAt,dispId = dispId, medicine=medicine,quantity = quantity)

                preg = 'Y' if preg_input else 'N'
                alcohol = 'Y' if alcohol_input else 'N'
                
                condition = current_obj['condition']
                message, return_obj = check_medicine(request, med_name, condition, preg, alcohol)
                # Check alcohol
                alcohol_msg = 'Positive. This medicine is safe for alcoholic person. '
                if alcohol == 'Y' and return_obj['alcohol'] == 'D':
                    alcohol_msg = 'Negative. This medicine is unsafe for alcoholic person. '
                # Check pregnancy
                preg_msg = 'Positive. This medicine is safe for pregnant woman. '
                if preg == 'Y' and return_obj['pregnant'] in {'C', 'D', 'X', 'N'}:
                    preg_msg = 'Negative. This medicine is unsafe for pregnant woman. '
                # Side effect
                side_effects_msg = return_obj['side_effects']
                # OTC
                rx_otc = return_obj['rx_otc']
                rx_otc_msg = 'Prescription needed for this medicine'
                if 'otc' in rx_otc:
                    rx_otc_msg = 'Available over the counter'

                messages.success(request, 'Drug name: ' + med_name)
                messages.success(request, 'Medical Condition: ' + condition)
                if alcohol_input:
                    messages.success(request, 'Alcohol: ' + alcohol_msg)
                if preg_input:
                    messages.success(request, 'Pregnancy: ' + preg_msg)
                messages.success(request, 'Side effects: ' + side_effects_msg)
                messages.success(request, 'Rx/OTC: ' + rx_otc_msg)

                if recommendation:
                    return_objs = recommend(condition, alcohol, preg)
                    for medicine in return_objs:
                        messages.success(request, ' ')
                        current_obj = medicine
                        condition = current_obj['condition']
                        med_name = current_obj['name']
                        message, return_obj = check_medicine(request, med_name, condition, preg, alcohol)
                        
                        side_effects_msg = return_obj['side_effects']
                        rx_otc = return_obj['rx_otc']
                        rx_otc_msg = 'Prescription needed for this medicine'
                        if 'otc' in rx_otc:
                            rx_otc_msg = 'Available over the counter'

                        messages.success(request, 'Drug name: ' + med_name)
                        messages.success(request, 'Medical Condition: ' + condition)
                        messages.success(request, 'Side effects: ' + side_effects_msg)
                        messages.success(request, 'Rx/OTC: ' + rx_otc_msg)
    context['form'] = form

    return render(request, 'home/dispense.html', context)

@login_required
def dispense_message(request):
    # Calculate the message
    message = 'You have dispensed your medicine!'
    return HttpResponse(message)

@login_required
def success(request):
    return render(request, 'home/success.html')

@login_required
def config(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            medicineA = str(form.cleaned_data['medicineA']).lower()
            medicineB = str(form.cleaned_data['medicineB']).lower()
            medicineC = str(form.cleaned_data['medicineC']).lower()
            quantityA = form.cleaned_data['quantityA']
            quantityB = form.cleaned_data['quantityB']
            quantityC = form.cleaned_data['quantityC']
            print(quantityA, quantityB, quantityC)
            
            # Check if the inputs are the same
            if medicineA == medicineB or medicineA == medicineC or medicineB == medicineC:
                message = "The inputs cannot be the same. Please try again."
                return render(request, 'home/config.html', {'message': message, 'form': form})
            
            # Check if the inputs are valid medicine name
            try:
                mdA = MedicineDetail.objects.get(pk=medicineA.lower())
            except MedicineDetail.DoesNotExist:
                message = "Medicine A is not exists."
                return render(request, 'home/config.html', {'message': message, 'form': form})
            try:
                mdB = MedicineDetail.objects.get(pk=medicineB.lower())
            except MedicineDetail.DoesNotExist:
                message = "Medicine B is not exists."
                return render(request, 'home/config.html', {'message': message, 'form': form})
            try:
                mdC = MedicineDetail.objects.get(pk=medicineC.lower())
            except MedicineDetail.DoesNotExist:
                message = "Medicine C is not exists."
                return render(request, 'home/config.html', {'message': message, 'form': form})
            
            # If correct inputs given, update the record
            obj1 = MedicalDispensor.objects.get(pk=1)
            obj1.medicine = medicineA
            obj1.quantity = quantityA
            obj1.save()

            obj2 = MedicalDispensor.objects.get(pk=2)
            obj2.medicine = medicineB
            obj2.quantity = quantityB
            obj2.save()

            obj3 = MedicalDispensor.objects.get(pk=3)
            obj3.medicine = medicineC
            obj3.quantity = quantityC
            obj3.save()


            # Store the form data in session
            request.session['medicineA'] = medicineA
            request.session['medicineB'] = medicineB
            request.session['medicineC'] = medicineC
            request.session['quantityA'] = quantityA
            request.session['quantityB'] = quantityB
            request.session['quantityC'] = quantityC

            message = "Setup successfully"
            return render(request, 'home/config.html', {'message': message, 'form': form})
    else:
        initial_values = {
            'medicineA': request.session.get('medicineA', ''),
            'medicineB': request.session.get('medicineB', ''),
            'medicineC': request.session.get('medicineC', ''),
            'quantityA': request.session.get('quantityA', ''),
            'quantityB': request.session.get('quantityB', ''),
            'quantityC': request.session.get('quantityC', ''),
        }
        form = ConfigForm(initial=initial_values)

    return render(request, 'home/config.html', {'form': form})

def displayMed(request):
    objects = MedicineDetail.objects.all()
    return render(request, 'home/displayMed.html', {'objects': objects})
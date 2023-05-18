from django import forms
#from .models import Medicine detail)
from .models import Dispenser

class DispenseForm(forms.Form):
    pregnancy = forms.BooleanField(required=False)
    #condition = forms.ModelChoiceField(queryset=(med deet).objects.all())
    alcohol = forms.BooleanField(required=False)
    recommendation = forms.BooleanField(required=False)
    dispenser_A = forms.BooleanField(label='Dispenser A', required=False)
    dispenser_B = forms.BooleanField(label='Dispenser B', required=False)
    dispenser_C = forms.BooleanField(label='Dispenser C', required=False)

class ConfigForm(forms.Form):
    medicineA = forms.CharField(label='Medicine A')
    medicineB = forms.CharField(label='Medicine B')
    medicineC = forms.CharField(label='Medicine C')

    quantityA = forms.IntegerField(label='Quantity A')
    quantityB = forms.IntegerField(label='Quantity B')
    quantityC = forms.IntegerField(label='Quantity C')


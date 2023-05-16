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


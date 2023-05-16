from django.urls import path
from medicine import views

urlpatterns=[
    path('medicine/add/', views.addMedicine, name = 'addMedicine'),
    path('medicine/<str:name>/', views.get_medicine, name='getMedicine'),
    path('medicine/<str:input_name>/<str:input_condition>/<str:input_alcohol>/<str:input_pregnant>/', views.check_medicine,  name='checkMedicine')
]
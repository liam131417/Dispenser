from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dispense/', views.dispense, name='dispense'),
    path('dispense_message/', views.dispense_message, name='dispense_message'),
    path('success/', views.success, name='success'),
    path('config/', views.config, name='config'),
    path('config/displayMed/', views.displayMed, name='displayMed'),
]

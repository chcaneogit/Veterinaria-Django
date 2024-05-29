
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('servicios', views.servicios, name='servicios'),
    path('registro', views.registro, name='registro'),
]
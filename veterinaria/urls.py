
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('servicios', views.servicios, name='servicios'),
    path('productos', views.productos, name='productos'),
    path('articulos', views.articulos, name='articulos'),
    path('carro', views.carro, name='carro'),
    path('registro', views.registro, name='registro'),
]

from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('productos/', views.productos, name='productos'),
    path('articulos/', views.articulos, name='articulos'),
    path('carro/', views.carro, name='carro'),
    path('registro/', views.registro, name='registro'),
    path('base/', views.base, name='base'),
    path('registroUsuario/', views.registroUsuario, name='registroUsuario'),
    path('crud/', views.crud, name='crud'),
    path('eliminar_usuario/<str:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios_findEdit/<str:pk>/', views.usuarios_findEdit, name='usuarios_findEdit'),
    path('usuarioUpdate', views.usuarioUpdate, name='usuarioUpdate'),
    path('login', login_view, name='login'),
    
]
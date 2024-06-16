
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
    path('productos/', views.productos, name='productos'),
    path('articulos/', views.articulos, name='articulos'),
    path('carro/', views.carro, name='carro'),
    path('base/', views.base, name='base'),
    #USUARIOS
    path('registro/', views.registro, name='registro'),
    path('crud/', views.crud, name='crud'),
    path('registroUsuario/', views.registroUsuario, name='registroUsuario'),
    path('eliminar_usuario/<str:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios_findEdit/<str:pk>/', views.usuarios_findEdit, name='usuarios_findEdit'),
    path('usuarioUpdate', views.usuarioUpdate, name='usuarioUpdate'),
    path('login', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    #PRODUCTOS
    path('registroProductos/', views.registroProductos, name='registroProductos'),
    path('productosAdd/', views.productosAdd, name='productosAdd'),
    path('productosCrud/', views.productosCrud, name='productosCrud'),
    path('eliminarProducto/<str:pk>/', views.eliminarProducto, name='eliminarProducto'),
    path('productos_findEdit/<str:pk>/', views.productos_findEdit, name='productos_findEdit'),
    path('productoUpdate/', views.productoUpdate, name='productoUpdate'),
    
]
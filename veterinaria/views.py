from django.shortcuts import render

# Create your views here.

def index(request):
    context={}
    return render(request, 'veterinaria/index.html', context)

def servicios(request):
    context={}
    return render(request, 'veterinaria/servicios.html', context)

def productos(request):
    context={}
    return render(request, 'veterinaria/productos.html', context)

def articulos(request):
    context={}
    return render(request, 'veterinaria/articulos.html', context)

def carro(request):
    context={}
    return render(request, 'veterinaria/carro.html', context)

def registro(request):
    context={}
    return render(request, 'veterinaria/registro.html', context)
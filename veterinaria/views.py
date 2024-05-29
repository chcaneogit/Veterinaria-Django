from django.shortcuts import render

# Create your views here.

def index(request):
    context={}
    return render(request, 'veterinaria/index.html', context)

def servicios(request):
    context={}
    return render(request, 'veterinaria/servicios.html', context)

def registro(request):
    context={}
    return render(request, 'veterinaria/registro.html', context)
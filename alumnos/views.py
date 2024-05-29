from django.shortcuts import render

# Create your views here.

def index(request):
    context={}
    return render(request, 'alumnos/index.html', context)

def servicios(request):
    context={}
    return render(request, 'alumnos/servicios.html', context)

def registro(request):
    context={}
    return render(request, 'alumnos/registro.html', context)
from django.shortcuts import render, redirect
from .forms import UsuarioForm
from django.contrib.auth.hashers import make_password

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

def base(request):
    context={}
    return render(request, 'veterinaria/base.html', context)

def prueba(request):
    context={}
    return render(request, 'veterinaria/prueba.html', context)

def registroUsuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(usuario.password)
            usuario.save()
            return redirect('index')  # Redirige a una página de éxito
    else:
        form = UsuarioForm()
    
    return render(request, 'veterinaria/registro.html', {'form': form})
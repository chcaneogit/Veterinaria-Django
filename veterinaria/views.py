from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Usuario 

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

def crud(request):
    context={}
    return render(request, 'veterinaria/crud.html', context)


def registroUsuario(request):
    if request.method == "POST":
        rut = request.POST["rut"]
        dv = request.POST["dv"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        correo = request.POST["correo"]
        nacimiento = request.POST["nacimiento"]
        celular = request.POST["celular"]
        direccion = request.POST["direccion"]
        password = request.POST["password"]

        if password == password:
            try:
                # Crear un usuario de Django
                user = User.objects.create_user(
                    username=correo,
                    password=password,
                    email=correo,
                    first_name=nombre,
                    last_name=apellido
                )

                # Crear el objeto Usuario en tu modelo personalizado
                obj = Usuario.objects.create(
                    rut=rut,
                    dv=dv,
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    nacimiento=nacimiento,
                    celular=celular,
                    direccion=direccion,
                    password=password  # Asegúrate de manejar correctamente la contraseña
                )

                # Guardar el objeto Usuario
                obj.save()

                

                # Redirigir a la página deseada después del registro
                return redirect('index')  

            except IntegrityError:
                # Manejar el caso donde el nombre de usuario (rut) ya existe
                return render(request, 'registro.html', {"error": "El rut ya está en uso."})

        else:
            # Manejar el caso donde las contraseñas no coinciden
            return render(request, 'registro.html', {"error": "Las contraseñas no coinciden."})

    else:
        # Renderizar el formulario de registro en el método GET
        return render(request, 'registro.html')
    
def crud(request):
    usuarios = Usuario.objects.all()
    context = {"usuarios": usuarios}
    return render(request, 'veterinaria/crud.html', context)

def eliminar_usuario(request, pk):
    context={}
    try:
        usuario = Usuario.objects.get(rut=pk)
        usuario.delete()
        mensaje = "¡Bien! Datos eliminados..."
        usuarios = usuario.objects.all()
        context = {'usuarios': usuarios, 'mensaje': mensaje}
        return render(request, 'veterinaria/crud.html', context)
    except:
        mensaje = "Error, el rut no existe..."
        usuarios = Usuario.objects.all()
        context = {'usuarios': usuarios, 'mensaje': mensaje}
        return render(request, 'veterinaria/crud.html', context)
    
def usuarios_findEdit(request, pk):
    
    if pk != "":
        usuario = Usuario.objects.get(rut=pk)
        
        context={'usuario':usuario}
        if usuario:
            return render(request, 'veterinaria/editar.html', context)
        else:
            context={'mensaje': "Error, rut no existe..."}
            return render(request, 'veterinaria/crud.html', context)     

def usuarioUpdate(request):
    if request.method == "POST":
        # Recupera los datos del formulario
        rut = request.POST["rut"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        correo = request.POST["correo"]
        celular = request.POST["celular"]
        direccion = request.POST["direccion"]
        password = request.POST["password"]
        
        # Recupera el usuario existente por su rut
        usuario = Usuario.objects.get(rut=rut)
        
        # Actualiza solo los campos que se han modificado en el formulario
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo
        usuario.celular = celular
        usuario.direccion = direccion
        usuario.password = password
        
        # Guarda los cambios
        usuario.save()
        
        context = {'mensaje': "Ok, datos actualizados...", 'usuario': usuario}
        return render(request, 'veterinaria/index.html', context)
    else:
        # Aquí manejas la lógica para cargar los datos del usuario a editar en el formulario
        usuarios = Usuario.objects.all()
        context = {'usuarios': usuarios}
        return render(request, 'veterinaria/crud.html', context)

def login_view(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        print(f'rut: {rut}, Password: {password}')

        # Verificar que el usuario existe
        try:
            user = User.objects.get(username=rut)
            print(f'User found: {user.username}, Active: {user.is_active}')
        except User.DoesNotExist:
            print('User does not exist')
            return render(request, 'veterinaria/articulos.html', {"error": "Credenciales incorrectas"})

        # Autenticar al usuario usando el campo rut
        user = authenticate(request, username=rut, password=password)
        print(f'User authenticated: {user}')

        if user is not None:
            login(request, user)
            print("Inicio de sesión exitoso")
            return redirect('index')
        else:
            print("Credenciales incorrectas")
            return render(request, 'veterinaria/articulos.html', {"error": "Credenciales incorrectas"})

    return render(request, 'veterinaria/servicios.html')
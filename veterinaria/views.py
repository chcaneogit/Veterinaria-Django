from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Usuario, Producto
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Create your views here.
def index(request):
    context={}
    return render(request, 'veterinaria/index.html', context)

def servicios(request):
    context={}
    return render(request, 'veterinaria/servicios.html', context)

def productos(request):
    #Muestra los productos llamándolos desde la BD, igual al crud
    productos = Producto.objects.all()
    context = {"productos": productos}
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

def productosAdd(request):
    context={}
    return render(request, 'veterinaria/productosAdd.html', context)

def productosEdit(request):
    context={}
    return render(request, 'veterinaria/productosEdit.html', context)

@login_required#Permite que la funcion solo se ejecute cuando el usuario esta logeado
def perfil(request):
    usuario = request.user  # Recupera el usuario actualmente autenticado
    context = {'usuario': usuario}
    return render(request, 'veterinaria/perfil.html', context)

#CRUD USUARIOS
def crud(request):
    usuarios = Usuario.objects.all()
    context = {"usuarios": usuarios}
    return render(request, 'veterinaria/crud.html', context)

def registroUsuario(request):
    #Obtiene los valores de los datos ingresados mediante POST
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

        try:
            # Verificar si el usuario ya existe por el rut
            if User.objects.filter(username=rut).exists():
                messages.error(request, "El RUT ya está en uso.")
                return render(request, 'veterinaria/registro.html')

            # Crear un usuario de Django
            user = User.objects.create_user(
                username=rut,
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
                password=make_password(password)  # Cifrar la contraseña
            )

            # Añadir mensaje de éxito
            messages.success(request, "Cuenta creada exitosamente.")
            # Redirigir a la página deseada después del registro
            return render(request, 'veterinaria/registro.html') 

        except IntegrityError:
            # Manejar el caso donde el nombre de usuario (rut) ya existe
            messages.error(request, "El RUT ya está en uso.")
            return render(request, 'veterinaria/registro.html')

    else:
        # Renderizar el formulario de registro en el método GET
        return render(request, 'veterinaria/registro.html')
    
def eliminar_usuario(request, pk):
    context={}
    
    try:#Elimina al usuario mediante la pk(RUT)
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
    #Función inicializa cuando se usar el boton editar en el CRUD
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
        # Recupera los datos del formulario mediante POST
        rut = request.POST["rut"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        correo = request.POST["correo"]
        celular = request.POST["celular"]
        direccion = request.POST["direccion"]
        password = request.POST["password"]
        
        # Recupera el usuario existente por su rut
        usuario = Usuario.objects.get(rut=rut)
        
        # Actualiza los campos
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.correo = correo
        usuario.celular = celular
        usuario.direccion = direccion
        
        # Si se proporciona una nueva contraseña, actualizarla
        if password:
            usuario.password = make_password(password)
        
        # Guarda los cambios
        usuario.save()
        
        # También actualiza el objeto User de Django si existe
        try:
            user = User.objects.get(username=rut)
            user.email = correo
            user.first_name = nombre
            user.last_name = apellido
            if password:
                user.set_password(password)  # Utiliza set_password para cifrar la contraseña
            user.save()
        except User.DoesNotExist:
            pass #Solo continúa
        
        context = {'mensaje': "Ok, datos actualizados...", 'usuario': usuario}
        return render(request, 'veterinaria/index.html', context)
    else:
        #Se maneja la lógica para cargar los datos del usuario a editar en el formulario
        usuarios = Usuario.objects.all()
        context = {'usuarios': usuarios}
        return render(request, 'veterinaria/crud.html', context)
    
def login_view(request):
    #Primero ferifica si existe el metodo POST
    if request.method == 'POST':
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        print(f'rut: {rut}, Password: {password}')
        
        # Verificar que el usuario existe
        try:
            user = User.objects.get(username=rut)
            print(f'Usuario ecnontrado: {user.username}, Activo: {user.is_active}')
        except User.DoesNotExist:
            print('Usuario no existe')
            return render(request, 'veterinaria/index.html', {"error": "RUT y/o contraseñas incorrecto"})

        # Autenticar al usuario usando el campo rut
        user = authenticate(request, username=rut, password=password)
        print(f'User authenticated: {user}')

        if user is not None:
            login(request, user)
            print("Inicio de sesión exitoso")
            return render(request, 'veterinaria/index.html')
        else:
            print("Credenciales incorrectas")
            return render(request, 'veterinaria/index.html', {"error": "RUT y/o contraseñas incorrecto"})

    return render(request, 'veterinaria/index.html')
#CRUD PRODUCTOS
def registroProductos(request):
    if request.method == "POST":
        codigo = request.POST["codigo"]
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        valor = request.POST["valor"]
        cantidad = request.POST["cantidad"]

        # Verificar si el código ya existe
        if Producto.objects.filter(codigo=codigo).exists():
            # Manejar el caso donde el código ya existe, y mostrar mensaje
            messages.error(request, "El código del producto ya existe.")
        else:
            try:
                # Crear una instancia del producto
                producto = Producto(
                    codigo=codigo,
                    nombre=nombre,
                    descripcion=descripcion,
                    valor=valor,
                    cantidad=cantidad
                )
                # Guardar el producto en la base de datos
                producto.save()
                # Añadir mensaje de éxito
                messages.success(request, "Producto registrado exitosamente.")
            except IntegrityError:
                # Manejar otros posibles errores de integridad
                messages.error(request, "Error al registrar el producto.")
        
        return render(request, 'veterinaria/productosAdd.html')
    else:
        return render(request, 'veterinaria/productosAdd.html')

def productosCrud(request):
    productos = Producto.objects.all()
    context = {"productos": productos}
    return render(request, 'veterinaria/ProductosCrud.html', context)

def eliminarProducto(request, pk):
    try:
        producto = Producto.objects.get(codigo=pk)
        producto.delete()
        mensaje = "¡Bien! Datos eliminados..."
    except Producto.DoesNotExist:
        mensaje = "Error, el producto no existe..."

    productos = Producto.objects.all()  
    context = {'productos': productos, 'mensaje': mensaje}  
    return render(request, 'veterinaria/productosCrud.html', context)

def productos_findEdit(request, pk):
    if pk != "":
        producto = Producto.objects.get(codigo=pk)
        
        context={'producto':producto}
        if producto:
            return render(request, 'veterinaria/productoEdit.html', context)
        else:
            context={'mensaje': "Error, codigo no existe..."}
            return render(request, 'veterinaria/productosCrud.html', context)     

def productoUpdate(request):
    if request.method == "POST":
        # Recupera los datos del formulario
        codigo = request.POST["codigo"]
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        valor = request.POST["valor"]
        cantidad = request.POST["cantidad"]
        
        try:
            # Recupera el producto existente por su código
            producto = Producto.objects.get(codigo=codigo)
        except Producto.DoesNotExist:
            # Manejar el caso donde el producto no existe
            messages.error(request, "El producto no existe.")
            productos = Producto.objects.all()
            context = {'productos': productos}
            return render(request, 'veterinaria/productosCrud.html', context)
        
        # Actualiza los campos
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.valor = valor
        producto.cantidad = cantidad
        producto.save()
        
        messages.success(request, "Producto actualizado exitosamente.")

        # Redirige a la lista de productos actualizada
        productos = Producto.objects.all()
        context = {'productos': productos}
        return render(request, 'veterinaria/productosCrud.html', context)
    
    else:
        # Maneja la lógica para cargar los datos del producto a editar en el formulario
        productos = Producto.objects.all()
        context = {'productos': productos}
        return render(request, 'veterinaria/productosCrud.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Usuario, Producto
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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

def registro(request):
    context={}
    return render(request, 'veterinaria/registro.html', context)

def base(request):
    context={}
    return render(request, 'veterinaria/base.html', context)

@login_required #Permite que la funcion solo se ejecute cuando el usuario esta logeado
def perfil(request):
    usuario = request.user  # Recupera el usuario actualmente autenticado
    context = {'usuario': usuario}
    return render(request, 'veterinaria/perfil.html', context)

#CRUD USUARIOS
@staff_member_required #Permite que la funcion solo se ejecute cuando el usuario staff esta logeado
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
                messages.error(request, "El RUT ya está en uso.") #Se usan mensajes para poder mostrarlos en la página
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

            messages.success(request, "Cuenta creada exitosamente.")
        
            return render(request, 'veterinaria/registro.html') 

        except IntegrityError:
            # Manejar el caso donde el nombre de usuario (rut) ya existe
            messages.error(request, "El RUT ya está en uso.")
            return render(request, 'veterinaria/registro.html')

    else:
    
        return render(request, 'veterinaria/registro.html')
    
@staff_member_required
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
@staff_member_required
def productosAdd(request):
    context={}
    return render(request, 'veterinaria/productosAdd.html', context)

@staff_member_required
def productosEdit(request):
    context={}
    return render(request, 'veterinaria/productosEdit.html', context)

@staff_member_required
def registroProductos(request):
    if request.method == "POST":
        codigo = request.POST["codigo"]
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        valor = request.POST["valor"]
        cantidad = request.POST["cantidad"]
        imagen = request.FILES.get('imagen', None)

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
                    cantidad=cantidad,
                    imagen=imagen
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

@staff_member_required
def productosCrud(request):
    productos = Producto.objects.all()
    context = {"productos": productos}
    return render(request, 'veterinaria/ProductosCrud.html', context)

@staff_member_required
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

@staff_member_required
def productos_findEdit(request, pk):
    if pk != "":
        producto = Producto.objects.get(codigo=pk)
        
        context={'producto':producto}
        if producto:
            return render(request, 'veterinaria/productoEdit.html', context)
        else:
            context={'mensaje': "Error, codigo no existe..."}
            return render(request, 'veterinaria/productosCrud.html', context)     

@staff_member_required
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

def agregar_al_carrito(request, producto_codigo):
    producto = Producto.objects.get(codigo=producto_codigo)
    carrito = request.session.get('carrito', [])

    # Variable para comprobar si el producto ya está en el carrito
    producto_encontrado = False
    
    # Verificar si el producto ya está en el carrito
    for item in carrito:
        if item['codigo'] == producto.codigo:
            if item['cantidad'] < 5:  
                item['cantidad'] += 1
            producto_encontrado = True
            break
    
    if not producto_encontrado :
        # Agregar el producto al carrito con la cantidad solicitada
        carrito.append({
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'cantidad': 1,
            'valor': producto.valor
        })
    
    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito

    return redirect('carro')

def carro(request):
    carrito = request.session.get('carrito', [])
    total_pago = 0
    total_iva = 0

    for item in carrito:
        item_total = item['valor'] * item['cantidad']
        item['total'] = item_total
        #Funciones para realizar cálculos
        total_pago += item_total
        total_iva = total_pago * 0.19
    #Se crea diccionario para poder llamar variables
    return render(request, 'veterinaria/carro.html', {'carrito': carrito, 'total_pago': total_pago, 'total_iva': total_iva})

def actualizar_cantidad(request, producto_codigo):
    carrito = request.session.get('carrito', [])
    accion = request.POST.get('accion')

    for item in carrito:
        if item['codigo'] == producto_codigo:
            if accion == 'sumar' and item['cantidad'] < 5:
                item['cantidad'] += 1
            elif accion == 'restar' and item['cantidad'] > 1:
                item['cantidad'] -= 1
            break

    request.session['carrito'] = carrito
    return redirect('carro')

def eliminar_del_carrito(request, producto_codigo):
    carrito = request.session.get('carrito', [])
    # Crear una nueva lista para los items que no serán eliminados
    nuevo_carrito = []
    # Iterar sobre cada item en el carrito
    for item in carrito:
        # Si el código del item es diferente al código del producto a eliminar
        if item['codigo'] != producto_codigo:
            # Agregar el item a la nueva lista
            nuevo_carrito.append(item)
    
    # Actualizar el carrito en la sesión con la nueva lista
    request.session['carrito'] = nuevo_carrito
    
    # Redirigir a la vista del carrito
    return redirect('carro')

def pagar_carrito(request):
    if request.method == "POST":
        carrito = request.session.get('carrito', [])
        # Lista para almacenar los productos que no tienen suficiente stock
        productos_no_disponibles = []

        for item in carrito:
            try:
                #Buscar producto por código
                producto = Producto.objects.get(codigo=item['codigo'])
                # Verificar si hay suficiente stock
                if producto.cantidad >= item['cantidad']:
                    #Reducir la cantidad del producto en stock
                    producto.cantidad -= item['cantidad']
                    producto.save()
                else:
                    # Añadir el producto a la lista de no disponibles con un mensaje detallado
                    productos_no_disponibles.append(f"{producto.nombre} (cantidad disponible: {producto.cantidad})")
            except Producto.DoesNotExist:
                productos_no_disponibles.append(item['nombre'])

        if productos_no_disponibles:
            # Usar join para concatenar los nombres de los productos no disponibles en un solo string
            mensajes_error = ", ".join(productos_no_disponibles)
            messages.error(request, f"No hay suficiente stock para los siguientes productos: {mensajes_error}.")
            return redirect('carro')

        # Vaciar el carrito después de la compra
        request.session['carrito'] = []
        messages.success(request, "Compra realizada exitosamente.")
        return redirect('carro')
    
    
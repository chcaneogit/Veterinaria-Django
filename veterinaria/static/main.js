function initMap() {
  var searchInput = document.querySelector('input[name="direccion"]');
  var autocomplete = new google.maps.places.Autocomplete(searchInput, { 
      types: ['geocode'],
      componentRestrictions: { country: 'cl' }
  }); 

  autocomplete.addListener('place_changed', function () { 
      var near_place = autocomplete.getPlace();
  });

  searchInput.addEventListener('keydown', function(event) {
      if (event.key === "Enter") {
          event.preventDefault(); 
          var place = autocomplete.getPlace();
          if (place && place.formatted_address) {
              searchInput.value = place.formatted_address;
          }
      }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
  const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
});


function validarTexto(idCampo) {
    let nombreInput = document.getElementById(idCampo);
    let nombre = nombreInput.value;
    let nombreError = document.getElementById(idCampo + "-error");
    let formulario = nombreInput.closest('form');

    if (nombre.length <=6) {
        nombreError.innerText = "Por favor, ingresa tu "+ idCampo;
        formulario.classList.remove('was-validated');
        return false;
    } else {
        nombreError.innerText = "";
        formulario.classList.add('was-validated');
        return true;
    }
}

function validarEdad(idCampo) {
    let fechaNacimientoInput = document.getElementById(idCampo);
    let fechaNacimiento = new Date(fechaNacimientoInput.value);
    let hoy = new Date();
    let nombreError = document.getElementById(idCampo + "-error");
    let formulario = fechaNacimientoInput.closest('form');

    // Calcular la edad en años
    let edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
    let mesActual = hoy.getMonth();
    let mesNacimiento = fechaNacimiento.getMonth();

    // Ajustar la edad si aún no se ha alcanzado el mes de nacimiento
    if (mesActual < mesNacimiento || (mesActual === mesNacimiento && hoy.getDate() < fechaNacimiento.getDate())) {
        edad=edad-1;
    }

    if (edad < 18) {
        nombreError.innerText = "Debe ser mayor a 18 años";
        formulario.classList.remove('was-validated');
        console.log(edad)
        return false;
        
    } else {
        nombreError.innerText = "";
        formulario.classList.add('was-validated');
        return true;
    }
}

function validarCelular(idCampo) {
    let celularInput = document.getElementById(idCampo);
    let celular = celularInput.value;

    // Verificar si el valor ingresado es numérico
    if (!/^\d+$/.test(celular)) {
        let celularError = document.getElementById(idCampo + "-error");
        let formulario = celularInput.closest('form');
        celularError.innerText = "Por favor, ingresa tu "+ idCampo;
        formulario.classList.remove('was-validated');
        return false;
    }

    let numero = parseInt(celular);
    let celularError = document.getElementById(idCampo + "-error");
    let formulario = celularInput.closest('form');
    if (numero < 9999999 || numero > 100000000) {
        celularError.innerText = "Por favor, ingresa tu "+ idCampo;
        formulario.classList.remove('was-validated');
        return false;
        
    } else {
        celularError.innerText = "";
        formulario.classList.add('was-validated');
        return true;
    }
    
}

function validarRutSinDv(idCampo) {
    let rutInput = document.getElementById(idCampo);
    let rut = rutInput.value;

    // Verificar si el valor ingresado es numérico
    if (!/^\d+$/.test(rut)) {
        let rutError = document.getElementById(idCampo + "-error");
        let formulario = rutInput.closest('form');
        rutError.innerText = "Por favor, ingresa tu " + idCampo + " sin puntos";
        formulario.classList.remove('was-validated');
        return false;
    }

    let numero = parseInt(rut);
    let rutError = document.getElementById(idCampo + "-error");
    let formulario = rutInput.closest('form');

    //Verificar el largo del rut sin puntos, guion y dígito verificador
    if (numero < 999999 || numero > 100000000) {
        rutError.innerText = "Por favor, ingresa tu " + idCampo;
        formulario.classList.remove('was-validated');
        return false;

    } else {
        rutError.innerText = "";
        formulario.classList.add('was-validated');
        return true;
    }
}

function validarDigitoVerificador(rutId, dvId) {
    // Obtener el valor del RUT y del dígito verificador
    var rut = document.getElementById(rutId).value;
    var dv = document.getElementById(dvId).value.toUpperCase(); // Convertir a mayúsculas para manejar K
    var dvError = document.getElementById(rutId + "-error"); 
    var formulario = document.getElementById(rutId).closest('form'); 
    // Calcular el dígito verificador esperado
    var suma = 0;
    var multiplo = 2;

    // Recorrer el cuerpo del RUT de derecha a izquierda
    for (var i = rut.length - 1; i >= 0; i--) {
        suma += parseInt(rut.charAt(i)) * multiplo;

        if (multiplo < 7) multiplo += 1;
        else multiplo = 2;
    }

    // Calcular el dígito verificador esperado
    var dvEsperado = 11 - (suma % 11);

    // Convertir el dígito verificador a string
    dvEsperado = (dvEsperado === 11) ? "0" : ((dvEsperado === 10) ? "K" : dvEsperado.toString());

    // Comparar el dígito verificador ingresado con el esperado
    if (dvEsperado !== dv) {
        dvError.innerText = "El RUT no es válido"; // Asignar mensaje de error al span de error
        formulario.classList.remove('was-validated'); // Remover la clase 'was-validated' del formulario
        return false;
    } else {
        dvError.innerText = ""; // Si no hay error, eliminar el mensaje de error
        formulario.classList.add('was-validated');
        return true;
    }
}

function validarFormulario() {
    // Llama funciones de validación individualmente
    const nombreValido = validarTexto('nombre');
    const correoValido = validarTexto('correo');
    const edadValida = validarEdad('nacimiento');
    const apellidoValido = validarTexto('apellido');
    const celularValido = validarCelular('celular');
    const contraseñaValida = validarTexto('password');
    const rutValido = validarTexto('rut');
    const direccionValida = validarTexto('direccion');

    // Si alguna validación falla, muestra un mensaje de error y devuelve false
    if (!(nombreValido && correoValido && edadValida && apellidoValido && celularValido && contraseñaValida && rutValido && direccionValida)) {
        alert('Por favor, completa todos los campos correctamente.');
        return false;
    }

    // Si todas las validaciones son exitosas, muestra una alerta indicando que la cuenta ha sido creada y devuelve true
    alert('¡Cuenta creada exitosamente!');
    return true;
}

$(document).ready(function(){
    $("#verMas1").click(function(){
      $(".articuloOculto1").toggle(); // Alternar la visibilidad del párrafo oculto
      if ($(this).text() === "Ver más") {
        $(this).text("Ver menos");
      } else {
        $(this).text("Ver más");
      }
    });
});
$(document).ready(function(){
    $("#verMas2").click(function(){
      $(".articuloOculto2").toggle(); // Alternar la visibilidad del párrafo oculto
      if ($(this).text() === "Ver más") {
        $(this).text("Ver menos");
      } else {
        $(this).text("Ver más");
      }
    });
});
$(document).ready(function(){
    $("#verMas3").click(function(){
      $(".articuloOculto3").toggle(); // Alternar la visibilidad del párrafo oculto
      if ($(this).text() === "Ver más") {
        $(this).text("Ver menos");
      } else {
        $(this).text("Ver más");
      }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const header = document.querySelector("header"); // ESTO ES EL NAVBAR

    header.innerHTML = `
    <nav class="navbar navbar-expand-lg fixed-top">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-veterinaria" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar-veterinaria">
          <a class="navbar-brand" href="index"><img class="logo-veterinaria img-thumbail" src="${logoUrl}" alt="Logo de veterinaria">Inicio</a>
          <ul class="navbar-nav ">
            <li class="nav-item">
              <a class="nav-link" href="servicios">Servicios</a>
              </li>
            <li class="nav-item">
              <a class="nav-link" href="productos">Productos</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="articulos">Articulos</a>
            </li>
            <li class="nav-item"> 
              <a class="nav-link" href="carro">Carrito</a>
            </li>
            <li class="nav-item">
            <li class="nav-item">
                <!-- Botón de Iniciar Sesión con Modal -->
              <button type="button" class="btn btn-link nav-link" data-bs-toggle="modal" data-bs-target="#loginModal">
                Iniciar Sesión
              </button>
              <!-- Fin del Botón de Iniciar Sesión con Modal -->
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <!-- MODAL INICIO DE SESION-->
      <div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="loginModalLabel">Inicio de Sesión</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form>
                <div class="col-md-8">
                  <label for="validationCustomUsername" class="form-label">Nombre Usuario</label>
                  <div class="input-group has-validation"> 
                    <input type="text" class="form-control" id="validationCustomUsername" aria-describedby="inputGroupPrepend" required>
                    <div class="invalid-feedback">
                      Introduzca nombre de usuario.
                    </div>
                  </div>
                </div>
                <div class="col-md-8">
                  <label for="validationCustomUsername" class="form-label">Contraseña</label>
                  <div class="input-group has-validation">
                    <input type="text" class="form-control" id="validationCustomUsername" aria-describedby="inputGroupPrepend" required>
                    <div class="invalid-feedback">
                      Instroduzca la contraseña.
                    </div>
                  </div>
                </div>
                <br>
                <button type="submit" class="btn btn-primary">Iniciar Sesión</button>
                <a href="registro" button type="submit" class="btn btn-primary">Registrarse</button></a>
              </form>
            </div>
          </div>
        </div>
      </div>
      <!--FIN MODAL INICIO DE SESION-->
    `;

    const footer = document.querySelector("footer"); // ESTO ES EL FOOTER
    footer.innerHTML = `
    <div class="container-fluid">
      <img class="logo-veterinaria img-thumbail" src="${logoUrl}"" >
      <a href="https://www.facebook.com"><i class="bi bi-facebook"></i></a>
      <a href="https://www.instagram.com"><i class="bi bi-instagram"></i></a>
      <a href="https://wa.me/56939635536"><i class="bi bi-whatsapp"></i></a>
    </div>
    `;
});


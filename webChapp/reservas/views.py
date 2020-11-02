from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from reservas.models import Habitacion, Reserva
from django.db.models import Q
from reservas.forms.reservas_forms import FormInicio, FormReserva, FormLoginUser
from reservas.util.utilities import calculoHabitaciones, generarLocalizador, calcularPrecio, sendConfirmEmail


# Impresión y validación del formulario.
def inicio(request):
    if request.method == 'POST':
        form = FormInicio(request.POST)
        if form.is_valid():                                       
            personas = form.cleaned_data['personas']
            fechaInicio = form.cleaned_data['fechainicio']
            fechaFin = form.cleaned_data['fechafin']
            request.session["data1"] = str(fechaInicio)
            request.session["data2"] = str(fechaFin)
            request.session["personas"] = str(personas)
            return redirect("seleccionhab")
    else:
        form = FormInicio

    return render(request, 'inicio.html', context = {'form':form})

# Seleccion de las habitaciones. Cáculo previo de las disponibles.
def seleccionHab(request):
    if request.method == 'POST':
        id_hab = request.POST["id"]
        request.session["idhab"] = id_hab
        return redirect("realizarReserva")

    fechaInicio = request.session["data1"] 
    fechaFin = request.session["data2"]
    personas = request.session["personas"]
    a = calculoHabitaciones(fechaInicio, fechaFin, personas)
    return render(request, "seleccion_habitacion.html", context={'habitaciones':a, 'fechainicio':fechaInicio, 'fechafin':fechaFin})


# último formulario para introducir los datos del cliente y creación de la reserva-
def realizarReserva(request):
    id_hab = request.session["idhab"]
    fsalida = request.session["data2"]
    fentrada = request.session["data1"]
    huespedes = request.session["personas"]
    habitacion = Habitacion.objects.get(id = id_hab)
    precioTotal = calcularPrecio(fentrada, fsalida, habitacion.precio)

    if request.method == 'POST':
        form = FormReserva(request.POST)
        
        if form.is_valid():
            localizador = generarLocalizador()
            reserva = Reserva.objects.create(fsalida = fsalida, 
                                    fentrada = fentrada,
                                    huespedes = huespedes,  
                                    email = form.cleaned_data['email'],
                                    nombre = form.cleaned_data['nombre'],
                                    telefono = form.cleaned_data['telefono'],
                                    precio = precioTotal,
                                    localizador = localizador,
                                    habitacion = habitacion)
            
            sendConfirmEmail(reserva)
            request.session["id_reserva"] = reserva.id
            return redirect('reservafin')
    else:
        form = FormReserva
    return render(request, "datos_cliente.html", context={'form':form,
                                                          'huespedes':huespedes,
                                                          'fsalida':fsalida,
                                                          'fentrada':fentrada,
                                                          'precio':precioTotal,
                                                          'tipo': habitacion.tipo})


# Muestra los datos de la reserva ya creada
def reservaFin(request):
    reserva = Reserva.objects.get(id = request.session["id_reserva"])
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, "reserva_fin.html", context={'reserva':reserva})


# Muestra los datos de una reserva en BBDD, previo login (el login no se guarda en sesión)
def mostraReserva(request):
    
    if request.method == 'POST':
        form = FormLoginUser(request.POST)
        if form.is_valid():
            reserva = Reserva.objects.filter(email = form.cleaned_data['email'], localizador = form.cleaned_data['localizador'])
            if reserva:
                return render(request, "mostrar_reserva.html", {'reserva':reserva})
            else:
                return render(request, "mostrar_reserva.html", {'login_error':'No se encuentra la reserva'})
    else:
        form = FormLoginUser
    
    return render(request, "mostrar_reserva.html", {'form':form})

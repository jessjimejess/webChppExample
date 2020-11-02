from reservas.models import Habitacion, Reserva
from django.db.models import Q
from dateutil.parser import parse
from django.core.mail import send_mail
import random
import string




def calculoHabitaciones(fechaInicio, fechaFin, personas):
    reservas = Reserva.objects.filter((Q(fentrada__lte = fechaInicio) & Q(fsalida__gte = fechaInicio)) | (Q(fentrada__lte = fechaFin) & Q(fsalida__gte = fechaFin))
                                        | (Q(fentrada__lte = fechaInicio) & Q(fsalida__gte = fechaFin)) | (Q(fentrada__gte = fechaInicio) & Q(fsalida__lte = fechaFin)))  ## Mejorar, añadir filtro de habitacion tambien
    habitaciones = Habitacion.objects.filter(tipo__gte = personas)
    habOcupadas = [0,0,0,0]
    lisHab = []

    for reserva in reservas:
        tipe = reserva.habitacion.tipo
        habOcupadas[int(tipe) - 1] =  habOcupadas[int(tipe) - 1] + 1

    for i,habitacion in enumerate(habitaciones):
        max_ = habitacion.numeromaxdisp
        disp = max_ - habOcupadas[habitacion.tipo - 1] 
        if disp > 0:
            lisHab.append(habitacion)

    return lisHab
    


def generarLocalizador():
    allascii = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(allascii) for i in range(6))
    return result



def calcularPrecio(fentrada, fsalida, precio):
    dif = parse(fsalida) - parse(fentrada)
    total = dif.days * precio
    return total



def sendConfirmEmail(reserva):
    try:
        send_mail("Prueba email de conformación: " + reserva.localizador, 'Detalles de tu reserva (vacío aposta)','hotelsinombre@gmail.com', [reserva.email], fail_silently=False)
    except Exception as e:
        print(e.__traceback__) 









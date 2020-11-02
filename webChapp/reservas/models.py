from django.db import models

# Las fechas se guardan en tipo Unix para facilitar los calculos.
# No es necesario llevar la cuenta de las habitacioens disponibles,
# es mas sencillo guardar el máximo de habitaciones por tipo y calcular las 
# disponibles cuando sea necesatio



class Habitacion(models.Model):
    tipo = models.IntegerField()
    precio = models.IntegerField()
    numeromaxdisp = models.IntegerField()

class Reserva(models.Model):
    fsalida = models.DateField()
    fentrada = models.DateField()
    huespedes = models.IntegerField()
    nombre = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    telefono = models.IntegerField()
    precio = models.IntegerField()
    localizador = models.CharField(max_length = 6)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)

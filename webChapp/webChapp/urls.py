"""webChapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name = 'inicio'),
    path("reservar/seleccionhab/", views.seleccionHab, name = 'seleccionhab'),
    path("reservar/realizareserva/", views.realizarReserva, name = 'realizarReserva'),
    path("reservar/fin/", views.reservaFin, name = 'reservafin'),
    path("mostrareserva/", views.mostraReserva, name = 'mostrareserva')
]+static(settings.STATIC_URL, document_rott = settings.STATIC_ROOT)

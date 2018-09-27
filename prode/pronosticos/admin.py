from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Equipo)
admin.site.register(Liga)
admin.site.register(EquipoLiga)
admin.site.register(Partido)
admin.site.register(Pronostico)
admin.site.register(Fecha)



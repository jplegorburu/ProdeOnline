from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Equipo)
admin.site.register(Liga)
admin.site.register(EquipoLiga)
admin.site.register(Partido)
admin.site.register(Fecha)
admin.site.register(FechaLiga)
admin.site.register(Torneo)
admin.site.register(UserTorneo)
admin.site.register(LigaTorneo)

@admin.register(Pronostico)
class PronosticoAdmin(admin.ModelAdmin):
    readonly_fields = ('resultado', )

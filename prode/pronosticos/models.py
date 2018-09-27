from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Equipo(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Liga(models.Model):
    TIPOS_LIGA = (
        ('temporada', 'Temporada'),
        ('copa','Copa'),
    )
    name = models.CharField(max_length=250)
    tipo = models.CharField(max_length=10, choices=TIPOS_LIGA, default='temporada')
    
    def __str__(self):
        return self.name

class EquipoLiga(models.Model):
    liga = models.ForeignKey(Liga, related_name='liga', on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, related_name='equipo', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('liga',)
    
    def __str__(self):
        return 'Equipo: {} Liga: {}'.format(self.equipo, self.liga)

class Fecha(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        try: 
            int(self.name)
            return "Fecha "+self.name
        except ValueError:
            return self.name

class FechaLiga(models.Model):
    fecha = models.ForeignKey(Fecha, related_name="fecha_liga", on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, related_name="liga_fecha", on_delete=models.CASCADE)

class Partido(models.Model):
    ESTADO_PARTIDO = (
        ('pendiente', 'Pendiente'),
        ('jugando', 'Jugando'),
        ('suspendido', 'Suspendido'),
        ('finalizado', 'Finalizado')
    )
    local= models.ForeignKey(Equipo, related_name='equipo_local', on_delete=models.CASCADE)
    local_gol= models.IntegerField()
    visita = models.ForeignKey(Equipo, related_name='equipo_visita', on_delete=models.CASCADE)
    visita_gol= models.IntegerField()
    fecha = models.DateField()
    hora = models.TimeField(null=True)
    fecha = models.ForeignKey(Fecha, related_name='fecha_partido',  on_delete=models.CASCADE)
    liga =  models.ForeignKey(Liga, related_name='liga_partido', on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, choices=ESTADO_PARTIDO, default='pendiente')

class Pronostico(models.Model):
    user = models.ForeignKey(User, related_name='user_pronostico', on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, related_name='partido_pronostico', on_delete=models.CASCADE)
    local_gol = models.IntegerField(default=0)
    visita_gol = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)



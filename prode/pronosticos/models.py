from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.urls import reverse
from django.db.models.signals import post_save, post_init, pre_save
# Create your models here.

class Equipo(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Fecha(models.Model):
    name = models.CharField(max_length=25)
    def __str__(self):
        try: 
            int(self.name)
            return "Fecha "+self.name
        except ValueError:
            return self.name

class Liga(models.Model):
    TIPOS_LIGA = (
        ('temporada', 'Temporada'),
        ('copa','Copa'),
    )
    name = models.CharField(max_length=250)
    tipo = models.CharField(max_length=10, choices=TIPOS_LIGA, default='temporada')
    equipos = models.ManyToManyField(Equipo, through='EquipoLiga')
    fechas = models.ManyToManyField(Fecha, through='FechaLiga')
    def __str__(self):
        return self.name

class EquipoLiga(models.Model):
    liga = models.ForeignKey(Liga, related_name='liga', on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, related_name='equipo', on_delete=models.CASCADE)
    class Meta:
        ordering = ('liga',)
        unique_together = ('equipo', 'liga')
    def __str__(self):
        return '{} - {}'.format(self.equipo, self.liga)

class FechaLiga(models.Model):
    fecha = models.ForeignKey(Fecha, related_name="fecha_liga", on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, related_name="liga_fecha", on_delete=models.CASCADE)
    def __str__(self):
        return '{} - {}'.format(self.fecha, self.liga)
    class Meta:
        unique_together = ('fecha', 'liga')

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
    dia = models.DateField()
    hora = models.TimeField(null=True)
    fecha = models.ForeignKey(Fecha, related_name='fecha_partido',  on_delete=models.CASCADE)
    liga =  models.ForeignKey(Liga, related_name='liga_partido', on_delete=models.CASCADE)
    estado = models.CharField(max_length=11, choices=ESTADO_PARTIDO, default='pendiente')
    estado_anterior = None

    def __str__(self):
        return '{} - {} - {} vs {}'.format(self.liga, self.fecha, self.local, self.visita)

    @staticmethod
    def post_save(sender, **kwargs):
        partido = kwargs.get('instance')
        if partido.estado_anterior != partido.estado and partido.estado == 'finalizado':
            for pronostico in Pronostico.objects.all().filter(partido=partido):
                pronostico.resultado = pronostico.puntos()
                pronostico.save()

    @staticmethod
    def guardar_estado(sender, **kwargs):
        partido = kwargs.get('instance')
        partido.estado_anterior = partido.estado

post_save.connect(Partido.post_save, sender=Partido)
post_init.connect(Partido.guardar_estado, sender=Partido)

class Torneo(models.Model):
    name = models.CharField(max_length=100, blank=False)
    admin = models.ForeignKey(User, related_name='admin_torneo', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through='UserTorneo')
    ligas = models.ManyToManyField(Liga, through='LigaTorneo')

    def get_users(self):
        ut= UserTorneo.objects.all().filter(user__in=self.users.all())
        users = []
        for u in ut:
            users.append(u.user)
        return users
    
    def get_ligas(self):
        lt = LigaTorneo.objects.all().filter(liga__in=self.ligas.all())
        ligas=[]
        for l in lt:
            ligas.append(l.liga)
        return ligas

class UserTorneo(models.Model):
    torneo = models.ForeignKey(Torneo, related_name='torneo_user', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_torneo', on_delete=models.CASCADE)
    class Meta:
        ordering = ('torneo',)
        unique_together = ('torneo', 'user')

class LigaTorneo(models.Model):
    torneo = models.ForeignKey(Torneo, related_name='torneo_liga', on_delete=models.CASCADE)
    liga = models.ForeignKey(Liga, related_name='liga_torneo', on_delete=models.CASCADE)
    class Meta:
        ordering = ('torneo',)
        unique_together = ('torneo', 'liga')

class Pronostico(models.Model):
    user = models.ForeignKey(User, related_name='user_pronostico', on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, related_name='partido_pronostico', on_delete=models.CASCADE)
    local_gol = models.IntegerField(default=0)
    visita_gol = models.IntegerField(default=0)
    resultado = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'partido',)

    def __str__(self):
        return 'Pronostico - {} - {}'.format(self.user, self.partido)
    
    def puntos(self):
        puntos = 0
        if self.acierto_ganador(self.partido) and self.partido.estado == 'finalizado':
            puntos += 1
            if self.acierto_resultado(self.partido):
                puntos += 2
        return puntos
    
    def acierto_ganador(self, partido):
        if self.local_gol > self.visita_gol and partido.local_gol > partido.visita_gol:
            return True
        if self.local_gol < self.visita_gol and partido.local_gol < partido.visita_gol:
            return True
        if self.local_gol == self.visita_gol and partido.local_gol == partido.visita_gol:
            return True
        return False

    def acierto_resultado(self, partido):
        if self.local_gol == partido.local_gol and self.visita_gol == partido.visita_gol:
            return True
        return False

    @staticmethod
    def pre_save(sender, **kwargs):
        pronostico = kwargs.get('instance')
        now = timezone.now()
        time_limit = timezone.timedelta(seconds=600)
        if pronostico.partido.dia > now.date():
            return
        elif pronostico.partido.dia == now.date() and pronostico.partido.hora >= (now + time_limit).time():
            return
        else:
            raise PermissionDenied()
pre_save.connect(Pronostico.pre_save, sender=Pronostico)




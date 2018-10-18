from rest_framework import serializers
from ..models import *

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

class EquipoLigaSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='equipo.id')
    name = serializers.ReadOnlyField(source='equipo.name')
    class Meta:
        model = EquipoLiga
        fields = ('id', 'name')

class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = ('id', 'name', 'tipo')

class LigaEquipoSerializer(serializers.ModelSerializer):
    equipos = EquipoLigaSerializer(source='liga', many=True)
    class Meta:
        model = Liga
        fields = ('id', 'name', 'equipos')

class PartidoSerializer(serializers.ModelSerializer):
    local = EquipoSerializer(many=False)
    visita = EquipoSerializer(many=False)
    class Meta:
        model = Partido
        fields = '__all__'

class FechaSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='fecha.id')
    name = serializers.ReadOnlyField(source='fecha.name')
    class Meta:
        model = FechaLiga
        fields = ('id', 'name')

class FechaLigaSerializer(serializers.ModelSerializer):
    fechas = FechaSerializer(source='liga_fecha', many=True)
    class Meta:
        model = Liga
        fields = ('id', 'name', 'fechas')

class PronosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pronostico
        fields = ('id', 'user', 'local_gol', 'visita_gol','partido')

class LigaTorneoSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='liga.id')
    name = serializers.ReadOnlyField(source='liga.name')
    class Meta:
        model = LigaTorneo
        fields = ('id', 'name')

class TorneoDetailSerializer(serializers.ModelSerializer):
    ligas = LigaTorneoSerializer(source='torneo_liga', many=True)
    class Meta:
        model = Torneo
        fields = ('id', 'name', 'admin', 'ligas', 'users')

class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = ('id', 'name', 'admin')
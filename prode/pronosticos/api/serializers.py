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
    pass
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
        fields = '__all__'

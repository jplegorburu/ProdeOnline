from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Equipo, Liga, EquipoLiga, Partido, Pronostico
from rest_framework.response import Response
from .serializers import EquipoSerializer, LigaSerializer, LigaEquipoSerializer, PartidoSerializer, FechaLigaSerializer, PronosticoSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import list_route, detail_route

class EquipoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class LigaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Liga.objects.all()

    def list(self, *args, **kwargs):
        self.serializer_class = LigaSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = LigaEquipoSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)

    @detail_route(methods=['get'])
    def top_10(self, request *args, **kwargs):
        liga = self.get_object()
        pronosticos = Pronostico.objects.all().filter(partido__liga=liga.id, partido__estado='finalizado')


class PartidoListView(generics.ListAPIView):
    serializer_class = PartidoSerializer
    
    def get_queryset(self):
        liga = self.kwargs['lk']
        fecha = self.kwargs['fk']
        return Partido.objects.filter(liga=liga, fecha=fecha)

class FechasListView(generics.RetrieveAPIView):
    queryset = Liga.objects.all()
    serializer_class = FechaLigaSerializer

class PartidoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('liga', 'fecha')

class PronosticoViewSet(viewsets.ModelViewSet):
    queryset = Pronostico.objects.all()
    serializer_class = PronosticoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'partido__liga', 'partido__fecha')

# class CommentPostView(APIView):
#     authentication_classes = (BasicAuthentication,)    
#     permission_classes = (IsAuthenticated,)
#     def post(self, request, pk, format=None):
#         post = get_object_or_404(Post, id=pk, status='published')
#         print (post)
#         com = Comment(post=post, name=request.user.username, email=request.user.email, body='Prueba curl')
#         com.save()
#         return Response({'comment': True})
from rest_framework import generics, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Equipo, Liga, EquipoLiga, Partido
from rest_framework.response import Response
from .serializers import EquipoSerializer, LigaSerializer, LigaEquipoSerializer, PartidoSerializer, FechaLigaSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class EquipoListView(generics.ListAPIView):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class LigaListView(generics.ListAPIView):
    queryset = Liga.objects.all()
    serializer_class = LigaSerializer

class LigaDetailView(generics.RetrieveAPIView):
    queryset = Liga.objects.all()
    serializer_class = LigaEquipoSerializer

class PartidoListView(generics.ListAPIView):
    serializer_class = PartidoSerializer
    
    def get_queryset(self):
        liga = self.kwargs['lk']
        fecha = self.kwargs['fk']
        return Partido.objects.filter(liga=liga, fecha=fecha)

class FechasListView(generics.RetrieveAPIView):
    queryset = Liga.objects.all()
    serializer_class = FechaLigaSerializer

# class CommentPostView(APIView):
#     authentication_classes = (BasicAuthentication,)    
#     permission_classes = (IsAuthenticated,)
#     def post(self, request, pk, format=None):
#         post = get_object_or_404(Post, id=pk, status='published')
#         print (post)
#         com = Comment(post=post, name=request.user.username, email=request.user.email, body='Prueba curl')
#         com.save()
#         return Response({'comment': True})
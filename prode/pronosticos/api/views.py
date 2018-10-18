from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Equipo, Liga, Partido, Pronostico, Torneo
from django.db.models import Sum, F
from rest_framework.response import Response
from .serializers import EquipoSerializer, LigaSerializer, LigaEquipoSerializer, PartidoSerializer, FechaLigaSerializer, PronosticoSerializer, TorneoDetailSerializer, TorneoSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
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
    def top_10(self, request, *args, **kwargs):
        liga = self.get_object()
        pronosticos = Pronostico.objects.all().filter(partido__liga=liga.id, partido__estado='finalizado')
        top= pronosticos.annotate(username = F('user__username')).values('username').annotate(total = Sum('resultado')).order_by('-total')[:10]
        return Response(top)

class TorneoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Torneo.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def list(self, *args, **kwargs):
        self.serializer_class = TorneoSerializer
        return viewsets.ModelViewSet.list(self, *args, **kwargs)
    
    @list_route(methods=['get'])
    def search(self, request, *args, **kwarfs):
        queryset = self.get_queryset()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        serializer = TorneoSerializer(queryset, many=True, context=self.get_serializer_context())    
        return Response(serializer.data)

    def retrieve(self, *args, **kwargs):
        self.serializer_class = TorneoDetailSerializer
        return viewsets.ModelViewSet.retrieve(self, *args, **kwargs)
    
    @detail_route(methods=['get'])
    def posiciones(self, request, *args, **kwargs):
        torneo = self.get_object()
        users = torneo.get_users()
        ligas = torneo.get_ligas()
        pronosticos = Pronostico.objects.all().filter(partido__liga__in=ligas, partido__estado='finalizado', user__in= users)
        posiciones = pronosticos.annotate(username = F('user__username')).values('username').annotate(total = Sum('resultado')).order_by('-total')
        return Response(posiciones)


class FechasListView(generics.RetrieveAPIView):
    queryset = Liga.objects.all()
    serializer_class = FechaLigaSerializer

class PartidoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('liga', 'fecha')

class PronosticoFilterSet(FilterSet):
    fecha = NumberFilter('partido__fecha')
    liga = NumberFilter('partido__liga')
    
    class Meta:
        model= Pronostico
        fields=('user', 'fecha', 'liga')

class PronosticoViewSet(viewsets.ModelViewSet):
    queryset = Pronostico.objects.all()
    serializer_class = PronosticoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PronosticoFilterSet
    filter_fields = ('user', 'liga', 'fecha')

# class CommentPostView(APIView):
#     authentication_classes = (BasicAuthentication,)    
#     permission_classes = (IsAuthenticated,)
#     def post(self, request, pk, format=None):
#         post = get_object_or_404(Post, id=pk, status='published')
#         print (post)
#         com = Comment(post=post, name=request.user.username, email=request.user.email, body='Prueba curl')
#         com.save()
#         return Response({'comment': True})
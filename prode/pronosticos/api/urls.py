from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('equipos', views.EquipoViewSet)
router.register('ligas', views.LigaViewSet)
router.register('partidos', views.PartidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('fechas/<pk>',
        views.FechasListView.as_view(),
        name='fechas_list'),
]
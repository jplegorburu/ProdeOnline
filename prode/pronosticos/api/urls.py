from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('equipos/',
         views.EquipoListView.as_view(),
         name='equipos_list'),

    path('liga/<pk>/',
         views.LigaDetailView.as_view(),
         name='ligas_detail'),
    
    path('liga/',
     views.LigaListView.as_view(),
     name='ligas_list'),
]
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post/',
         views.PostListView.as_view(),
         name='post_list'),

    path('post/<pk>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    
    path('post/<pk>/comment/',
     views.CommentPostView.as_view(),
     name='post_comment'),
]
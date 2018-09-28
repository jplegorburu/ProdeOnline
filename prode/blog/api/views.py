from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Post, Comment
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentPostView(APIView):
    authentication_classes = (BasicAuthentication,)    
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        post = get_object_or_404(Post, id=pk, status='published')
        print (post)
        com = Comment(post=post, name=request.user.username, email=request.user.email, body='Prueba curl')
        com.save()
        return Response({'comment': True})
        

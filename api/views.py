from rest_framework import generics
from rest_framework.views import APIView

from .models import Post
from rest_framework import permissions
from .serializer import PostSerializer
from rest_framework.permissions import IsAuthenticated
class IsAuthenticatedAndTokenHasScope(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'access_token' in request.auth

class PostsView(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedAndTokenHasScope]
    class PostList(generics.ListAPIView):

        queryset = Post.objects.all()
        serializer_class = PostSerializer

    class PostDetail(generics.RetrieveAPIView):

        queryset = Post.objects.all()
        serializer_class = PostSerializer

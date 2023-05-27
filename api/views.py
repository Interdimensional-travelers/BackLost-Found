from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
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

    class AddPostView(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
            jwt_authentication = JWTAuthentication()
            user, _ = jwt_authentication.authenticate(request)

            # Retrieve the user ID
            author_id = user.id

            # Create the post with the provided data
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author_id=author_id)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
    class EditPostView(APIView):

        def put(self, request, post_id):
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({'detail': 'Post not found'}, status=404)
            jwt_authentication = JWTAuthentication()
            user, _ = jwt_authentication.authenticate(request)
            # Check if the current user is the author of the post
            if post.author != user:
                return Response({'detail': 'You do not have permission to edit this post'}, status=403)

            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    class DeletePostView(APIView):

        def delete(self, request, post_id):
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({'detail': 'Post not found'}, status=404)
            jwt_authentication = JWTAuthentication()
            user, _ = jwt_authentication.authenticate(request)
            # Check if the current user is the author of the post
            if post.author != user:
                return Response({'detail': 'You do not have permission to delete this post'}, status=403)

            post.delete()
            return Response({'detail': 'Post deleted successfully'})
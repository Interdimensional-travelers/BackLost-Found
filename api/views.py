from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import PostSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


class IsAuthenticatedAndTokenHasScope(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'access_token' in request.auth


class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data.get('email', '')
            user = User.objects.create_user(username=username, password=password, email=email)
            return Response({'detail': 'User created successfully'})
        return Response(serializer.errors, status=400)


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


class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the client's IP address
        ip = request.META.get('REMOTE_ADDR')

        # Define the rate limit key
        rate_limit_key = f'ratelimit:{ip}'

        # Get the current request count
        request_count = cache.get(rate_limit_key, 0)

        # Check if the rate limit is exceeded
        if request_count >= 150:
            return HttpResponse("Too Many Requests", status=429)

        # Increment the request count
        cache.set(rate_limit_key, request_count + 1, 60)  # 60 seconds = 1 minute

        # Allow the request to proceed
        return None

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"detail": "Logout successful"})
        except Exception as e:
            return Response({"detail": "Logout failed"}, status=400)
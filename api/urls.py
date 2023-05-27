
from django.urls import path, include
from . import views
from .views import CreateUserView

urlpatterns = [
    path('posts/', views.PostsView.PostList.as_view()),
    path('post/<int:pk>/', views.PostsView.PostDetail.as_view()),
    path('addpost/', views.PostsView.AddPostView.as_view(), name='add_post'),
    path('editpost/<int:post_id>/', views.PostsView.EditPostView.as_view(), name='edit-post'),
    path('deletepost/<int:post_id>/', views.PostsView.DeletePostView.as_view(), name='delete-post'),
    path('createuser/', CreateUserView.as_view(), name='create-user'),
]


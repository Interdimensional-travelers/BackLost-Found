
from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.PostsView.PostList.as_view()),
    path('post/<int:pk>/', views.PostsView.PostDetail.as_view()),
    path('addpost/', views.PostsView.AddPostView.as_view(), name='add_post'),
]


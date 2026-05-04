from django.urls import path
from .views import (blog,
                   post_list_view,
                   post_detail_view,
                   create_post_view,
                   edit_post_view,
                   PostListView,
                   PostDetailView,
                   PostCreateView,
                   PostUpdateView,
                   PostDeleteView,
                   )

app_name = 'blog' # Определяем пространство имен для этого приложения

# Этот список urlpatterns будет подключен к главному urls.py проекта
urlpatterns = [
    path('', blog),

    path('post_list/', post_list_view, name='post_list'),
    path('post_detail/<int:pk>/', post_detail_view, name='post_detail'),
    path('create_post/', create_post_view, name='create_post'),
    path('edit_post/<int:pk>/', edit_post_view, name='edit_post'),

    path('post_lst/', PostListView.as_view(), name='post_lst'),
    path('post_dtl/<int:pk>/', PostDetailView.as_view(), name='post_dtl'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),


]

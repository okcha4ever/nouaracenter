from django.urls import path, include
from django.contrib import admin
from . import views
from django.views.generic import TemplateView



urlpatterns = [
    path('', views.redirect_home, name='redirect_home'),
    path('home', views.home, name='view-home'),
    path('create', views.create, name='create'),
    path('update/<post_id>', views.update, name='update'),
    path('delete/<post_id>', views.delete, name='delete'),
    path('like', views.like, name='like-post'),
    path('<int:pk>/comments', views.CommentView.as_view(), name='comments'),
    path('<int:pk>/comment', views.AddCommentView.as_view(), name='comment'),
    path('<int:pk>/delete_comment', views.delete_comment, name='delete-comment'),
]

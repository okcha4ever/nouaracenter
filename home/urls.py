from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('', include('django.contrib.auth.urls')),
    path('', include('members.urls')),
    path('posts/', include('posts.urls')),
]

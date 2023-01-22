from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.signout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

]

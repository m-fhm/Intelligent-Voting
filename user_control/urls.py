from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.lgout, name='logout'),
    path('home/', views.home, name='home'),

]

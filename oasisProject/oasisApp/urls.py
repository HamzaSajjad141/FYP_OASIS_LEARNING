from django.urls import path
from . import views
urlpatterns = [
   path('', views.Home,name='Home'),
   path('Login/', views.Login,name='Login'),
   path('RegisterPage/', views.Register,name='Register'),
   
]

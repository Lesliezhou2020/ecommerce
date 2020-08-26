from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('men', views.men),
    path('women', views.women),
]

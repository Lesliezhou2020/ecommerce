from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('men', views.men),
    path('women', views.women),
    path('admin/', views.admin),
    path('admin/dashboard', views.admin_dash),
    path('admin/login', views.admin_login),
    path('admin/logout', views.admin_logout),
    path('product/add', views.add_product),
    path('register', views.register),
    path('login', views.login),
    path('user_create', views.user_create),
    path('carts', views.carts)
]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('register_guest/', views.register_guest_view, name='register_guest'),
    path('recover_password/', views.recover_password_view, name='recover_password'),
    path('logout/', views.logout_view, name='logout'),
]


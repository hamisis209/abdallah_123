from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login', views.login_view),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-login', views.admin_login_view),
    path('register/', views.register_view, name='register'),
    path('register', views.register_view),
    path('register_guest/', views.register_guest_view, name='register_guest'),
    path('register_guest', views.register_guest_view),
    path('recover_password/', views.recover_password_view, name='recover_password'),
    path('recover_password', views.recover_password_view),
    path('logout/', views.logout_view, name='logout'),
    path('logout', views.logout_view),
    path('profile/', views.profile_view, name='profile'),
    path('profile', views.profile_view),
]


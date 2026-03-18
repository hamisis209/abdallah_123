from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('performance/', views.performance_view, name='performance'),
    path('search/', views.search_view, name='search'),
]


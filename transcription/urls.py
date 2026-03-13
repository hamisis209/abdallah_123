from django.urls import path
from . import views

urlpatterns = [
    path('transcribe/', views.transcribe_view, name='transcribe'),
    path('offline_transcribe/', views.offline_transcribe, name='offline_transcribe'),
]


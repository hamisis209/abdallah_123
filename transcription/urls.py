from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import TranscriptViewSet, TranscriptionSessionViewSet

router = DefaultRouter()
router.register(r'transcripts', TranscriptViewSet)
router.register(r'sessions', TranscriptionSessionViewSet)

urlpatterns = [
    path('transcribe/', views.transcribe_view, name='transcribe'),
    path('offline_transcribe/', views.offline_transcribe, name='offline_transcribe'),
    path('api/', include(router.urls)),
]


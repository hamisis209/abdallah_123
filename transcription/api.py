from rest_framework import viewsets
from .models import Transcript, TranscriptionSession
from .serializers import TranscriptSerializer, TranscriptionSessionSerializer

class TranscriptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TranscriptSerializer
    queryset = Transcript.objects.all()

    def get_queryset(self):
        return Transcript.objects.filter(user=self.request.user)

class TranscriptionSessionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TranscriptionSessionSerializer
    queryset = TranscriptionSession.objects.all()

    def get_queryset(self):
        return TranscriptionSession.objects.filter(user=self.request.user)
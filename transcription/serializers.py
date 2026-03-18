from rest_framework import serializers
from .models import Transcript, TranscriptionSession

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['id', 'title', 'original_audio', 'transcript_text', 'language', 'duration', 'word_count', 'confidence_score', 'processing_time', 'created_at']

class TranscriptionSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionSession
        fields = ['id', 'session_id', 'language', 'started_at', 'ended_at', 'total_duration', 'transcript_count']
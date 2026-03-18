from django.db import models
from django.contrib.auth.models import User

class Transcript(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    original_audio = models.FileField(upload_to='transcripts/audio/', blank=True, null=True)
    transcript_text = models.TextField()
    language = models.CharField(max_length=10, choices=[
        ('en', 'English'),
        ('sw', 'Swahili'),
    ], default='en')
    duration = models.FloatField(help_text="Duration in seconds", null=True, blank=True)
    word_count = models.PositiveIntegerField(default=0)
    confidence_score = models.FloatField(null=True, blank=True)
    processing_time = models.FloatField(help_text="Processing time in seconds", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.transcript_text:
            self.word_count = len(self.transcript_text.split())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.title or 'Untitled'} ({self.language})"

class TranscriptionSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    language = models.CharField(max_length=10, default='en')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    total_duration = models.FloatField(default=0)
    transcript_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Session {self.session_id}"
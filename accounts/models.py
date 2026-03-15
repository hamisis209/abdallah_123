from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    GENDER_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("non_binary", "Non-binary"),
        ("prefer_not_say", "Prefer not to say"),
        ("other", "Other"),
    ]
    DISABILITY_CHOICES = [
        ("none", "No disability"),
        ("visual", "Visual"),
        ("hearing", "Hearing"),
        ("mobility", "Mobility"),
        ("learning", "Learning"),
        ("speech", "Speech"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    student_id = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=30, blank=True, choices=GENDER_CHOICES)
    program = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    emergency_contact_name = models.CharField(max_length=120, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)
    disability_status = models.CharField(
        max_length=20, choices=DISABILITY_CHOICES, default="none"
    )
    disability_description = models.TextField(blank=True)
    assistive_devices = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

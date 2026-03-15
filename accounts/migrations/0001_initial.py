from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, max_length=50)),
                ('gender', models.CharField(blank=True, choices=[('female', 'Female'), ('male', 'Male'), ('non_binary', 'Non-binary'), ('prefer_not_say', 'Prefer not to say'), ('other', 'Other')], max_length=30)),
                ('program', models.CharField(blank=True, max_length=150)),
                ('phone_number', models.CharField(blank=True, max_length=30)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=120)),
                ('country', models.CharField(blank=True, max_length=120)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=120)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=30)),
                ('disability_status', models.CharField(choices=[('none', 'No disability'), ('visual', 'Visual'), ('hearing', 'Hearing'), ('mobility', 'Mobility'), ('learning', 'Learning'), ('speech', 'Speech'), ('other', 'Other')], default='none', max_length=20)),
                ('disability_description', models.TextField(blank=True)),
                ('assistive_devices', models.CharField(blank=True, max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

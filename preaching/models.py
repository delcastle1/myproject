from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class CustomUser(AbstractUser):
    is_preacher = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
    )

    def __str__(self):
        return self.username

class GospelSong(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('audio', 'Audio'),
        ('video', 'Video')
    ]

    title = models.CharField(max_length=100)
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_artist': True})
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES, default='audio')
    file = models.FileField(upload_to='gospel_songs/')
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class PreacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=200)
    description = models.TextField()

class PreachingSession(models.Model):
    SESSION_TIMES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    scheduled_date = models.DateField()
    session_time = models.CharField(max_length=10, choices=SESSION_TIMES)
    is_live = models.BooleanField(default=False)
    preacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_preacher': True})
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

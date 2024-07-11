from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class GospelSong(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('audio', 'Audio'),
        ('video', 'Video')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]

    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES, default='audio')
    file = models.FileField(upload_to='gospel_songs/')
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title
    
class Quiz(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.question 

class Preacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name



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
    preacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

class Visitor(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.artist.username} - {self.count} visitors"
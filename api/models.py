from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'country', 'contact']

class ChurchProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = CloudinaryField('image', folder='church_projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    CATEGORY_CHOICES = [
        ('prophecy', 'Prophecy'),
        ('crusades', 'Crusades'),
        ('testimonies', 'Testimonies'),
        ('healings', 'Healings'),
        ('prayers', 'Prayers for Viewers'),
        ('mass_prayers', 'Mass Prayers'),
        ('deliverance', 'Deliverance'),
        ('charities', 'Charities'),
        ('praise', 'Praise'),
        ('worship', 'Worship'),
    ]
    
    title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.category}"

class InspirationQuote(models.Model):
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quote[:50]

class PrayerRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    request = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prayer Request from {self.name}"

class Testimony(models.Model):
    name = models.CharField(max_length=255)
    testimony_text = models.TextField(null=True, blank=True)
    testimony_video = CloudinaryField('video', folder='testimonies', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Testimony from {self.name}"

class UpcomingEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = CloudinaryField('image', folder='events')
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 
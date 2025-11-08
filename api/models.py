from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import URLValidator


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
    image = models.ImageField(upload_to='projects/', max_length=500)
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


class Stream(models.Model):
    STREAM_TYPE_CHOICES = [
        ('live', 'YouTube Live'),
        ('regular', 'YouTube Video'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stream_type = models.CharField(max_length=10, choices=STREAM_TYPE_CHOICES, default='live')
    youtube_url = models.URLField(
        validators=[URLValidator()],
        help_text="URL of the YouTube video or live stream"
    )
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = 'Active' if self.is_active else 'Inactive'
        return f"{self.title} - {status} ({self.get_stream_type_display()})"
        
    def clean(self):
        if not self.youtube_url:
            raise ValidationError('YouTube URL is required')
        # You might want to add additional validation for YouTube URL format

class PrayerRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    request = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prayer Request from {self.name}"

def testimony_video_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/testimonies/<filename>
    return f'testimonies/{filename}'

class Testimony(models.Model):
    name = models.CharField(max_length=255)
    testimony_text = models.TextField(null=True, blank=True)
    testimony_video = models.FileField(
        upload_to=testimony_video_upload_path,
        max_length=500,
        help_text='Upload a video file (MP4, WebM, OGG)'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimony from {self.name}"

class UpcomingEvent(models.Model):
    EVENT_STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', max_length=500)
    event_date = models.DateTimeField()
    event_status = models.CharField(max_length=10, choices=EVENT_STATUS_CHOICES, default='upcoming')
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.title} - {self.get_event_status_display()}" 

class PrayerRoom(models.Model):
    """Singleton model to represent the prayer room with YouTube streaming."""
    title = models.CharField(max_length=200, default="Prayer Room", help_text="Title of the prayer room")
    description = models.TextField(blank=True, null=True, help_text="Description of the prayer room")
    is_active = models.BooleanField(default=False, help_text="Whether the prayer room is currently active")
    youtube_url = models.URLField(
        validators=[URLValidator()],
        help_text="YouTube URL for the prayer stream (live or recorded)",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    current_topic = models.CharField(max_length=200, default="General Prayer", help_text="Current prayer topic or focus")

    class Meta:
        verbose_name = 'Prayer Room'
        verbose_name_plural = 'Prayer Room'

    def __str__(self):
        return f"Prayer Room ({'Active' if self.is_active else 'Inactive'})"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and PrayerRoom.objects.exists():
            # Update existing instance instead of creating new one
            existing = PrayerRoom.objects.first()
            existing.title = self.title
            existing.description = self.description
            existing.current_topic = self.current_topic
            existing.youtube_url = self.youtube_url
            return existing.save(*args, **kwargs)
        return super().save(*args, **kwargs)

    @classmethod
    def get_prayer_room(cls):
        """Get the single prayer room instance, create it if it doesn't exist"""
        if not cls.objects.exists():
            return cls.objects.create()
        return cls.objects.first() 

# Courses/Modules/Videos hierarchy
class Course(models.Model):
    CATEGORY_CHOICES = [
        ('sons_of_john_chi', 'Sons of John Chi'),
        ('mentorship', 'Mentorship'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', max_length=500)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='modules/', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course.name}"

class CourseVideo(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    name = models.CharField(max_length=255)
    description = models.TextField()
    youtube_url = models.URLField()
    key_takeaways = models.TextField(blank=True, null=True)
    assignments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.module.name}"
    
    def get_youtube_thumbnail(self):
        """Extract YouTube video ID and return thumbnail URL"""
        import re
        # Extract video ID from various YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                video_id = match.group(1)
                return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None

class Comment(models.Model):
    video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.name}"

class Devotion(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField()
    text_content = models.TextField(blank=True, null=True, help_text="Devotional text content")
    youtube_url = models.URLField(blank=True, null=True, help_text="YouTube video URL")
    devotion_date = models.DateField(help_text="Date for this devotion")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-devotion_date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.devotion_date}"
    
    def get_youtube_thumbnail(self):
        """Extract YouTube video ID and return thumbnail URL"""
        if self.content_type == 'video' and self.youtube_url:
            import re
            patterns = [
                r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.youtube_url)
                if match:
                    video_id = match.group(1)
                    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None

class CourseApplication(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('sons_of_john_chi', 'Sons of John Chi'),
        ('mentorship', 'Mentorship'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Application details
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Personal information
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    your_interest = models.TextField(help_text="Why are you interested in this course?")
    your_goals = models.TextField(help_text="What are your goals?")
    
    # User credentials
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, help_text="Password will be hashed")
    
    # Related user (created after approval)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='application')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    
    class Meta:
        ordering = ['-created_at']
        # Allow same email for different application types, but not for the same type
        unique_together = [['email', 'application_type']]
    
    def __str__(self):
        return f"{self.full_name} - {self.get_application_type_display()} ({self.get_status_display()})"
from rest_framework import serializers
from .models import (
    User, ChurchProject, Video, InspirationQuote, 
    PrayerRequest, Testimony, UpcomingEvent, Course, Module, CourseVideo, Comment, Devotion,
    CourseApplication, Stream, PrayerRoom
)
from django.contrib.auth.hashers import make_password

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'country', 'contact', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            country=validated_data['country'],
            contact=validated_data['contact']
        )
        return user

class ChurchProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurchProject
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class InspirationQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspirationQuote
        fields = '__all__'

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = [
            'id', 'title', 'description', 'stream_url',
            'thumbnail_url', 'scheduled_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_stream_url(self, value):
        """
        Validate that the stream URL is from a supported platform.
        """
        supported_domains = [
            'youtube.com', 'youtu.be',  # YouTube
            'facebook.com', 'fb.watch',  # Facebook
            'vimeo.com',                # Vimeo
            'twitch.tv'                 # Twitch
        ]
        
        if not any(domain in value for domain in supported_domains):
            raise serializers.ValidationError(
                "Please provide a valid streaming URL from a supported platform. "
                "Supported platforms: YouTube, Facebook, Vimeo, Twitch."
            )
            
        # Additional validation for YouTube URLs
        if 'youtube.com' in value or 'youtu.be' in value:
            if 'youtube.com/watch?v=' not in value and 'youtu.be/' not in value:
                if 'youtube.com/live/' not in value:  # Allow YouTube live URLs
                    raise serializers.ValidationError(
                        "Please provide a valid YouTube video or live stream URL."
                    )
                    
        return value

class PrayerRoomSerializer(serializers.ModelSerializer):
    """Serializer for the PrayerRoom model with YouTube streaming."""
    class Meta:
        model = PrayerRoom
        fields = [
            'id', 'title', 'description', 'is_active', 'current_topic',
            'youtube_url', 'created_at', 'updated_at', 'started_at', 'ended_at'
        ]
        read_only_fields = [
            'id', 'is_active', 'created_at', 'updated_at', 
            'started_at', 'ended_at'
        ]

    def validate_youtube_url(self, value):
        """Validate that the URL is a valid YouTube URL."""
        if not value:
            return value
            
        # Basic URL validation is done by the URLField
        # Additional YouTube URL validation can be added here if needed
        return value
        read_only_fields = ['is_active', 'start_time', 'end_time', 'created_at', 'updated_at']
    
    def validate(self, data):
        if not data.get('youtube_url'):
            raise serializers.ValidationError("YouTube URL is required")
        # You might want to add additional validation for YouTube URL format
        return data

class PrayerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = '__all__'

class TestimonySerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimony
        fields = '__all__'
        extra_kwargs = {
            'testimony_video': {
                'required': False,
                'allow_null': True
            }
        }

class UpcomingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingEvent
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class CourseVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVideo
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    user_has_replied = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'video', 'user', 'parent', 'text', 'created_at', 
            'replies', 'reply_count', 'user_has_replied'
        ]
        read_only_fields = ['user', 'created_at', 'replies', 'reply_count', 'user_has_replied']
    
    def get_replies(self, obj):
        # Only return replies if explicitly requested to avoid n+1 queries
        if 'replies' in self.context.get('include', []):
            return CommentSerializer(
                obj.replies.all().order_by('created_at'), 
                many=True,
                context={'include': []}  # Don't include nested replies
            ).data
        return []
    
    def get_reply_count(self, obj):
        return obj.replies.count()
    
    def get_user_has_replied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.replies.filter(user=request.user).exists()
        return False
    
    def validate(self, data):
        # For replies, ensure the parent comment exists and belongs to the same video
        parent = data.get('parent')
        video = data.get('video')
        
        if parent and video and parent.video_id != video.id:
            raise serializers.ValidationError({
                'parent': 'Parent comment must belong to the same video.'
            })
            
        return data

class DevotionSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Devotion
        fields = ['id', 'title', 'content_type', 'description', 'text_content', 
                  'youtube_url', 'devotion_date', 'created_at', 'thumbnail_url']
        read_only_fields = ['created_at', 'thumbnail_url']
    
    def get_thumbnail_url(self, obj):
        return obj.get_youtube_thumbnail()
    
    def validate(self, data):
        """Ensure appropriate content is provided based on content_type"""
        content_type = data.get('content_type')
        
        if content_type == 'text' and not data.get('text_content'):
            raise serializers.ValidationError({
                'text_content': 'Text content is required when content_type is "text"'
            })
        
        if content_type == 'video' and not data.get('youtube_url'):
            raise serializers.ValidationError({
                'youtube_url': 'YouTube URL is required when content_type is "video"'
            })
        
        return data

class CourseApplicationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = CourseApplication
        fields = ['id', 'application_type', 'status', 'full_name', 'email', 'phone_number',
                  'your_interest', 'your_goals', 'username', 'password', 'user', 'user_details',
                  'created_at', 'updated_at', 'reviewed_at', 'reviewed_by']
        read_only_fields = ['status', 'user', 'user_details', 'created_at', 'updated_at', 
                           'reviewed_at', 'reviewed_by']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        # Store the plain password for user creation after approval
        plain_password = validated_data.pop('password', None)
        validated_data['password'] = make_password(plain_password)
        return super().create(validated_data)
    
    def validate_username(self, value):
        """Check if username already exists in User or CourseApplication"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if CourseApplication.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use by another application.")
        return value
    
    def validate(self, data):
        """Check if user already has a pending or approved application for this type"""
        email = data.get('email')
        application_type = data.get('application_type')
        
        # Check if there's an existing pending or approved application for this email and type
        existing_app = CourseApplication.objects.filter(
            email=email, 
            application_type=application_type,
            status__in=['pending', 'approved']
        ).first()
        
        if existing_app:
            if existing_app.status == 'pending':
                raise serializers.ValidationError({
                    'email': f'You already have a pending application for {application_type}.'
                })
            elif existing_app.status == 'approved':
                raise serializers.ValidationError({
                    'email': f'Your application for {application_type} has already been approved.'
                })
        
        return data
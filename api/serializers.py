from rest_framework import serializers
from .models import (
    User, ChurchProject, Video, InspirationQuote,
    PrayerRequest, Testimony, UpcomingEvent, Course, Module, CourseVideo, Comment, Devotion
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'country', 'email', 'contact', 'username', 'password')
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

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

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
    
    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'parent', 'text', 'created_at', 'replies']
        read_only_fields = ['user', 'created_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

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
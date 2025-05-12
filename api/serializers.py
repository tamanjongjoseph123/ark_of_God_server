from rest_framework import serializers
from .models import (
    User, ChurchProject, Video, InspirationQuote,
    PrayerRequest, Testimony, UpcomingEvent
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
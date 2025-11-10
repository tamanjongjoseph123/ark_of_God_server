from rest_framework import serializers
from .models import DeviceToken

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ['token']
        extra_kwargs = {
            'token': {'validators': []}  # Disable unique validation to handle it in the view
        }

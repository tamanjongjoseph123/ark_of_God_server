from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import PrayerRoom
from .serializers import PrayerRoomSerializer

class PrayerRoomViewSet(viewsets.ViewSet):
    """
    API endpoint for managing the prayer room with YouTube streaming.
    """
    permission_classes = [permissions.AllowAny]
    
    def get_prayer_room(self):
        """Get or create the single prayer room instance"""
        return PrayerRoom.get_prayer_room()

    def list(self, request):
        """Get the current prayer room status"""
        prayer_room = self.get_prayer_room()
        serializer = PrayerRoomSerializer(prayer_room)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Get the current prayer room status (same as list)"""
        return self.list(request)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Returns the active prayer room status.
        This endpoint is publicly accessible.
        """
        prayer_room = self.get_prayer_room()
        if not prayer_room.is_active:
            return Response(
                {'status': 'No active prayer room'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PrayerRoomSerializer(prayer_room)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def start(self, request):
        """
        Start the prayer room with a YouTube URL.
        Only accessible by admin users.
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can start the prayer room'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        youtube_url = request.data.get('youtube_url')
        title = request.data.get('title', 'Prayer Room')
        description = request.data.get('description', '')
        current_topic = request.data.get('current_topic', 'General Prayer')
        
        # Validate YouTube URL
        if not youtube_url:
            return Response(
                {'error': 'YouTube URL is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            URLValidator()(youtube_url)
        except ValidationError:
            return Response(
                {'error': 'Please enter a valid URL'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        prayer_room = self.get_prayer_room()
        if prayer_room.is_active:
            return Response(
                {'error': 'The prayer room is already active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update prayer room details
        prayer_room.title = title
        prayer_room.description = description
        prayer_room.current_topic = current_topic
        prayer_room.youtube_url = youtube_url
        prayer_room.is_active = True
        prayer_room.started_at = timezone.now()
        prayer_room.ended_at = None
        prayer_room.save()
        
        return Response({
            'status': 'Prayer room started',
            'is_active': True,
            'youtube_url': youtube_url,
            'started_at': prayer_room.started_at,
            'current_topic': current_topic
        })

    @action(detail=False, methods=['post'])
    def end(self, request):
        """
        End the prayer room.
        Only accessible by admin users.
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can end the prayer room'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        prayer_room = self.get_prayer_room()
        if not prayer_room.is_active:
            return Response(
                {'error': 'The prayer room is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        prayer_room.is_active = False
        prayer_room.ended_at = timezone.now()
        prayer_room.save()
        
        return Response({
            'status': 'Prayer room ended',
            'is_active': False,
            'ended_at': prayer_room.ended_at
        })

    @action(detail=False, methods=['post'])
    def update_topic(self, request):
        """
        Update the current prayer topic.
        Only accessible by admin users.
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can update the prayer topic'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        prayer_room = self.get_prayer_room()
        new_topic = request.data.get('topic')
        
        if not new_topic:
            return Response(
                {'error': 'Topic is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        prayer_room.current_topic = new_topic
        prayer_room.save()
        
        return Response({
            'status': 'Prayer topic updated',
            'current_topic': new_topic
        })

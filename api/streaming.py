from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Stream
from .serializers import StreamSerializer

class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'active':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Only show active streams to non-admin users and unauthenticated users
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            return Stream.objects.filter(is_active=True)
        return Stream.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def start(self, request, pk=None):
        stream = self.get_object()
        if stream.is_active:
            return Response(
                {'status': 'Stream is already active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stream.start_time = timezone.now()
        stream.is_active = True
        stream.save()
        
        return Response({'status': 'Stream started'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def end(self, request, pk=None):
        stream = self.get_object()
        if not stream.is_active:
            return Response(
                {'status': 'Stream is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stream.end_time = timezone.now()
        stream.is_active = False
        stream.save()
        
        return Response({'status': 'Stream ended'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def active(self, request):
        active_stream = Stream.objects.filter(is_active=True).first()
        if active_stream:
            serializer = self.get_serializer(active_stream)
            return Response(serializer.data)
        return Response({'status': 'No active stream'}, status=status.HTTP_404_NOT_FOUND)

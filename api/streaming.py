from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Stream
from .serializers import StreamSerializer


class StreamViewSet(viewsets.ModelViewSet):
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']  # Allow DELETE method

    def get_queryset(self):
        # Only ever return the single stream
        return Stream.objects.all()[:1]

    def get_object(self):
        # Always return the single stream, creating it if it doesn't exist
        return Stream.get_stream()

    def list(self, request, *args, **kwargs):
        # Redirect list view to retrieve the single stream
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Don't allow creating new streams, only updating the existing one
        return Response(
            {'detail': 'Method not allowed. Use PUT or PATCH to update the existing stream.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the current stream"""
        stream = self.get_object()
        serializer = self.get_serializer(stream)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def current(self, request):
        """Public endpoint to get the current stream (no auth required)"""
        stream = self.get_object()
        serializer = self.get_serializer(stream)
        return Response(serializer.data)
        
    def destroy(self, request, *args, **kwargs):
        """
        Delete the stream.
        A new empty stream will be automatically created when needed.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import (
    User, ChurchProject, Video, InspirationQuote,
    PrayerRequest, Testimony, UpcomingEvent, Course, Module, CourseVideo, Comment, Devotion
)
from .serializers import (
    UserSerializer, ChurchProjectSerializer, VideoSerializer,
    InspirationQuoteSerializer, PrayerRequestSerializer,
    TestimonySerializer, UpcomingEventSerializer, UserLoginSerializer,
    CourseSerializer, ModuleSerializer, CourseVideoSerializer, CommentSerializer, DevotionSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=400)

class ChurchProjectViewSet(viewsets.ModelViewSet):
    queryset = ChurchProject.objects.all()
    serializer_class = ChurchProjectSerializer
    permission_classes = [AllowAny]

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category = request.query_params.get('category', None)
        if category:
            videos = self.queryset.filter(category=category)
            serializer = self.get_serializer(videos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter is required'}, status=400)

class InspirationQuoteViewSet(viewsets.ModelViewSet):
    queryset = InspirationQuote.objects.all().order_by('-created_at')
    serializer_class = InspirationQuoteSerializer
    permission_classes = [AllowAny]

class PrayerRequestViewSet(viewsets.ModelViewSet):
    queryset = PrayerRequest.objects.all().order_by('-created_at')
    serializer_class = PrayerRequestSerializer
    permission_classes = [AllowAny]

class TestimonyViewSet(viewsets.ModelViewSet):
    queryset = Testimony.objects.all().order_by('-created_at')
    serializer_class = TestimonySerializer
    permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

# Custom permission: admins can write, others read-only
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class UpcomingEventViewSet(viewsets.ModelViewSet):
    queryset = UpcomingEvent.objects.all().order_by('-event_date')
    serializer_class = UpcomingEventSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filter by event status
        event_status = self.request.query_params.get('event_status')
        if event_status:
            qs = qs.filter(event_status=event_status)
        
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            qs = qs.filter(location__icontains=location)
        
        return qs
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get only upcoming events"""
        upcoming_events = self.queryset.filter(event_status='upcoming')
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Get only past events"""
        past_events = self.queryset.filter(event_status='past')
        serializer = self.get_serializer(past_events, many=True)
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all().order_by('-created_at')
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs

class CourseVideoViewSet(viewsets.ModelViewSet):
    queryset = CourseVideo.objects.all().order_by('-created_at')
    serializer_class = CourseVideoSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        module_id = self.request.query_params.get('module')
        if module_id:
            qs = qs.filter(module_id=module_id)
        return qs

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent__isnull=True).order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        video_id = self.request.query_params.get('video')
        if video_id:
            qs = qs.filter(video_id=video_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DevotionViewSet(viewsets.ModelViewSet):
    queryset = Devotion.objects.all().order_by('-devotion_date', '-created_at')
    serializer_class = DevotionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filter by content type
        content_type = self.request.query_params.get('content_type')
        if content_type:
            qs = qs.filter(content_type=content_type)
        
        # Filter by date
        date = self.request.query_params.get('date')
        if date:
            qs = qs.filter(devotion_date=date)
        
        # Get today's devotion
        if self.request.query_params.get('today') == 'true':
            from datetime import date as dt_date
            qs = qs.filter(devotion_date=dt_date.today())
        
        return qs
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's devotions (can be multiple)"""
        from datetime import date as dt_date
        today_devotions = self.queryset.filter(devotion_date=dt_date.today())
        if today_devotions.exists():
            serializer = self.get_serializer(today_devotions, many=True)
            return Response(serializer.data)
        return Response({'detail': 'No devotions for today'}, status=404)
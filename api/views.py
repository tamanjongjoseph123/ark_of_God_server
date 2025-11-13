import logging
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from notifications.views import send_push_notification
from django.utils import timezone

from .models import (
    User, ChurchProject, Video, InspirationQuote, 
    PrayerRequest, Testimony, UpcomingEvent,
    Course, Module, CourseVideo, Comment, Devotion, CourseApplication, Stream, PrayerRoom
)
from .serializers import (
    UserSerializer, ChurchProjectSerializer, VideoSerializer, 
    InspirationQuoteSerializer, PrayerRequestSerializer, TestimonySerializer,
    UpcomingEventSerializer, CourseSerializer, ModuleSerializer, 
    CourseVideoSerializer, CommentSerializer, DevotionSerializer, 
    CourseApplicationSerializer, StreamSerializer, PrayerRoomSerializer, UserLoginSerializer
)

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # First try to authenticate the user
        user = authenticate(username=username, password=password)
        
        # Check if this is a staff/admin user
        if user is not None and user.is_staff:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'is_admin': True
            })
        
        # Check if this is a course application user
        try:
            application = CourseApplication.objects.get(username=username)
            
            # First check if the application is approved and user exists
            if application.status == 'approved' and application.user:
                if user is not None:  # If authentication was successful
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': UserSerializer(user).data,
                        'is_admin': False
                    })
                else:
                    # If authentication failed but application is approved
                    return Response(
                        {'error': 'Invalid username or password. Please try again.'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            
            # Check if the password matches the one in the application
            if not application.password or not check_password(password, application.password):
                return Response(
                    {'error': 'Invalid username or password. Please try again.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # If we get here, the password is correct but the application is not approved
            if application.status == 'pending':
                return Response(
                    {'error': 'Your application is still under review. Please wait for approval.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            elif application.status == 'rejected':
                return Response(
                    {'error': 'Your application has been rejected. Please contact support for more information.'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # This should not normally be reached
            return Response(
                {'error': 'There was an issue with your account. Please contact support.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        except CourseApplication.DoesNotExist:
            # No application found with this username
            pass
        
        # If we get here, either:
        # 1. No application found with this username, or
        # 2. Password didn't match
        return Response(
            {'error': 'Invalid username or password. Please try again.'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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
        video_id = self.request.query_params.get('video_id')
        include_replies = self.request.query_params.get('include_replies', '').lower() == 'true'
        
        qs = self.queryset
        if video_id:
            qs = qs.filter(video_id=video_id)
        
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        if self.action == 'retrieve' or 'include_replies' in self.request.query_params:
            context['include'] = ['replies']
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Create a reply to a comment"""
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the reply
        reply = serializer.save(
            user=request.user,
            video=parent_comment.video,
            parent=parent_comment
        )
        
        # Get the updated parent comment with replies
        parent_comment.refresh_from_db()
        return Response(
            self.get_serializer(parent_comment).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get all replies for a comment"""
        comment = self.get_object()
        replies = comment.replies.all().order_by('created_at')
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)

class DevotionViewSet(viewsets.ModelViewSet):
    queryset = Devotion.objects.all().order_by('-devotion_date', '-created_at')
    serializer_class = DevotionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        logger = logging.getLogger('api.views')
        try:
            # Save the devotion
            devotion = serializer.save()
            
            # Prepare and send notification
            title = "New Devotion Available"
            preview = (devotion.description[:47] + '...') if len(devotion.description) > 50 else devotion.description
            body = f"{devotion.title} - {preview}"
            
            data = {
                'type': 'new_devotion',
                'devotion_id': str(devotion.id),
                'title': devotion.title,
                'description': devotion.description,
                'content_type': devotion.content_type,
                'devotion_date': devotion.devotion_date.isoformat() if devotion.devotion_date else None,
                'created_at': timezone.now().isoformat(),
            }
            
            if devotion.content_type == 'video' and devotion.youtube_url:
                data['youtube_url'] = devotion.youtube_url
            
            # Send push notification
            send_push_notification(title, body, data)
            
            return devotion
            
        except Exception as e:
            logger.exception("Error creating devotion or sending notification")
            raise

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
        today_devotions = self.queryset.filter(devotion_date=timezone.now().date())
        serializer = self.get_serializer(today_devotions, many=True)
        return Response(serializer.data)
        today_devotions = self.queryset.filter(devotion_date=dt_date.today())
        if today_devotions.exists():
            serializer = self.get_serializer(today_devotions, many=True)
            return Response(serializer.data)
        return Response({'detail': 'No devotions for today'}, status=404)

class CourseApplicationViewSet(viewsets.ModelViewSet):
    queryset = CourseApplication.objects.all().order_by('-created_at')
    serializer_class = CourseApplicationSerializer
    
    def get_permissions(self):
        """Allow anyone to create applications, but only admins can view/update"""
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filter by application type
        application_type = self.request.query_params.get('application_type')
        if application_type:
            qs = qs.filter(application_type=application_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        
        return qs
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """Approve an application and create/update user account"""
        application = self.get_object()
        
        if application.status == 'approved':
            return Response(
                {'detail': 'Application is already approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = None
            # If application was previously rejected, check if user exists
            if application.status == 'rejected' and application.user:
                user = application.user
                # Update user details from application
                user.email = application.email
                user.contact = application.phone_number
                user.name = application.full_name
                user.save()
            
            # If no user exists, create a new one
            if not user:
                user = User(
                    username=application.username,
                    email=application.email,
                    country=application.country if hasattr(application, 'country') else '',
                    contact=application.phone_number,
                    name=application.full_name
                )
                # Set the password directly (it's already hashed)
                user.password = application.password
                user.save()
            
            # Update application
            application.status = 'approved'
            application.user = user
            application.reviewed_by = request.user
            from django.utils import timezone
            application.reviewed_at = timezone.now()
            application.save()
            
            serializer = self.get_serializer(application)
            return Response({
                'detail': 'Application approved successfully',
                'application': serializer.data
            })
        except Exception as e:
            return Response(
                {'detail': f'Error processing approval: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """Reject an application"""
        application = self.get_object()
        
        if application.status == 'rejected':
            return Response(
                {'detail': 'Application is already rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'rejected'
        application.reviewed_by = request.user
        from django.utils import timezone
        application.reviewed_at = timezone.now()
        application.save()
        
        # If there was a user created, we don't delete it but keep it for reference
        # The user can be reactivated if the application is approved again
        
        serializer = self.get_serializer(application)
        return Response({
            'detail': 'Application rejected',
            'application': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending applications"""
        pending_apps = self.queryset.filter(status='pending')
        serializer = self.get_serializer(pending_apps, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def approved(self, request):
        """Get all approved applications"""
        approved_apps = self.queryset.filter(status='approved')
        serializer = self.get_serializer(approved_apps, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login for approved applicants"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if application exists and is approved
        try:
            application = CourseApplication.objects.get(username=username)
            if application.status != 'approved':
                return Response(
                    {'error': 'Your application is not yet approved'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # If we have a user linked to the application, try to authenticate with that user
            if application.user:
                user = authenticate(request, username=application.user.username, password=password)
                if user is not None:
                    # Generate JWT token
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': UserSerializer(user).data,
                        'application_type': application.application_type
                    })
                
                # If authentication failed, check if it's a password issue
                if User.objects.filter(username=username).exists():
                    return Response(
                        {'error': 'Incorrect password'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                return Response(
                    {'error': 'Authentication failed'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except CourseApplication.DoesNotExist:
            return Response(
                {'error': 'No application found with this username'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Fallback to standard authentication if no user is linked
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            # Check if user exists but password is wrong
            if User.objects.filter(username=username).exists():
                return Response(
                    {'error': 'Incorrect password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(
                {'error': 'User account not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'application_type': application.application_type
        })
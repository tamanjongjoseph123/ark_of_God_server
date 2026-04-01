from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ChurchProjectViewSet, VideoViewSet,
    InspirationQuoteViewSet, PrayerRequestViewSet, TestimonyViewSet,
    UpcomingEventViewSet, CourseViewSet, ModuleViewSet, CourseVideoViewSet,
    CommentViewSet, DevotionViewSet, CourseApplicationViewSet, LoginView, VideoTranslationViewSet
)
from .streaming import StreamViewSet
from .prayer_room import PrayerRoomViewSet

router = SimpleRouter()
router.register(r'church-projects', ChurchProjectViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'inspiration-quotes', InspirationQuoteViewSet)
router.register(r'prayer-requests', PrayerRequestViewSet)
router.register(r'testimonies', TestimonyViewSet)
router.register(r'upcoming-events', UpcomingEventViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'course-videos', CourseVideoViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'devotions', DevotionViewSet)
router.register(r'applications', CourseApplicationViewSet)
router.register(r'video-translations', VideoTranslationViewSet)
router.register(r'stream', StreamViewSet, basename='stream')

# Single prayer room endpoints
prayer_room_router = SimpleRouter()
prayer_room_router.register(r'', PrayerRoomViewSet, basename='prayer-room')

# API URL patterns - these will be included under /api/
urlpatterns = [
    # Authentication - using re_path to ensure exact match
    re_path(r'^auth/login/$', LoginView.as_view(), name='admin-login'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Public stream endpoint (no auth required)
    path('stream/current/', StreamViewSet.as_view({'get': 'current'}), name='stream-current'),
    
    # Prayer room endpoints
    path('prayer-room/', include(prayer_room_router.urls)),
    
    # Include all router URLs
    path('', include(router.urls)),
]

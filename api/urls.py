from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChurchProjectViewSet, VideoViewSet,
    InspirationQuoteViewSet, PrayerRequestViewSet, TestimonyViewSet,
    UpcomingEventViewSet, LoginView, CourseViewSet, ModuleViewSet, CourseVideoViewSet,
    CommentViewSet, DevotionViewSet
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login', LoginView.as_view()),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]

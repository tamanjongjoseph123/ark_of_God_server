from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, LoginView, ChurchProjectViewSet, VideoViewSet,
    InspirationQuoteViewSet, PrayerRequestViewSet, TestimonyViewSet,
    UpcomingEventViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'church-projects', ChurchProjectViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'inspiration-quotes', InspirationQuoteViewSet)
router.register(r'prayer-requests', PrayerRequestViewSet)
router.register(r'testimonies', TestimonyViewSet)
router.register(r'upcoming-events', UpcomingEventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

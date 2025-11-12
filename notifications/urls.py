from django.urls import path
from . import views

urlpatterns = [
    path('register-device/', views.register_device_token, name='register-device'),
    path('test-notification/', views.test_notification, name='test-notification'),
]

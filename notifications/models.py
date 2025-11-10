from django.db import models
from django.utils import timezone

class DeviceToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device Token: {self.token[:10]}..."

    class Meta:
        verbose_name = "Device Token"
        verbose_name_plural = "Device Tokens"

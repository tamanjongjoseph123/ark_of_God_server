from django.contrib import admin
from .models import DeviceToken

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('token_short', 'created_at', 'last_used')
    list_filter = ('created_at', 'last_used')
    search_fields = ('token',)
    readonly_fields = ('created_at', 'last_used')
    
    def token_short(self, obj):
        return f"{obj.token[:15]}..." if obj.token else "-"
    token_short.short_description = 'Token (truncated)'

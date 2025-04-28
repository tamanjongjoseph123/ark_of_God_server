from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, ChurchProject, Video, InspirationQuote,
    PrayerRequest, Testimony, UpcomingEvent
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'country', 'contact', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'country')
    search_fields = ('username', 'email', 'country', 'contact')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'country', 'contact')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'country', 'contact'),
        }),
    )

@admin.register(ChurchProject)
class ChurchProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'youtube_url')
    list_filter = ('category', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(InspirationQuote)
class InspirationQuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'created_at')
    search_fields = ('quote',)
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country', 'created_at')
    search_fields = ('name', 'email', 'country', 'request')
    list_filter = ('country', 'created_at')
    date_hierarchy = 'created_at'

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'testimony_text')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(UpcomingEvent)
class UpcomingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('event_date', 'created_at')
    date_hierarchy = 'event_date'

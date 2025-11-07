from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, ChurchProject, Video, InspirationQuote,
    PrayerRequest, Testimony, UpcomingEvent, Course, Module, CourseVideo, Comment, Devotion
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
    list_display = ('title', 'event_status', 'event_date', 'location', 'created_at')
    search_fields = ('title', 'description', 'location')
    list_filter = ('event_status', 'event_date', 'created_at')
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_status', 'location')
        }),
        ('Media & Date', {
            'fields': ('image', 'event_date')
        }),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('name', 'description', 'course__name')

@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'created_at')
    list_filter = ('module', 'created_at')
    search_fields = ('name', 'description', 'module__name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'text_preview', 'parent', 'created_at')
    list_filter = ('created_at', 'video')
    search_fields = ('user__username', 'text', 'video__name')
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'

@admin.register(Devotion)
class DevotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'devotion_date', 'created_at')
    list_filter = ('content_type', 'devotion_date', 'created_at')
    search_fields = ('title', 'description', 'text_content')
    date_hierarchy = 'devotion_date'
    ordering = ('-devotion_date', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content_type', 'description', 'devotion_date')
        }),
        ('Content', {
            'fields': ('text_content', 'youtube_url'),
            'description': 'Provide text_content for text devotions or youtube_url for video devotions'
        }),
    )

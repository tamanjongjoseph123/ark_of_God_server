from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, ChurchProject, Video, InspirationQuote, 
    PrayerRequest, Testimony, UpcomingEvent, 
    Course, Module, CourseVideo, Comment, Devotion, CourseApplication, Stream, PrayerRoom
)
from django.utils import timezone

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
    list_display = ('name', 'created_at', 'video_preview')
    search_fields = ('name', 'testimony_text')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('video_preview',)
    fieldsets = (
        (None, {
            'fields': ('name', 'testimony_text')
        }),
        ('Video Testimony', {
            'fields': ('testimony_video', 'video_preview')
        }),
    )

    def video_preview(self, obj):
        if obj.testimony_video:
            video_html = (
                '<video width="320" height="240" controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>'
            )
            return format_html(video_html, obj.testimony_video.url)
        return "No video uploaded"
    video_preview.short_description = 'Video Preview'

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

@admin.register(CourseApplication)
class CourseApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'application_type', 'status', 'email', 'phone_number', 'created_at')
    list_filter = ('application_type', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'username', 'phone_number')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'password')
    
    fieldsets = (
        ('Application Details', {
            'fields': ('application_type', 'status')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'your_interest', 'your_goals')
        }),
        ('Account Credentials', {
            'fields': ('username', 'password'),
            'description': 'Password is hashed and cannot be viewed'
        }),
        ('Review Information', {
            'fields': ('user', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        """Bulk approve applications"""
        from django.utils import timezone
        approved_count = 0
        
        for application in queryset.filter(status='pending'):
            try:
                # Create user account
                user = User.objects.create_user(
                    username=application.username,
                    email=application.email,
                    password=application.password,
                    country='',
                    contact=application.phone_number
                )
                
                application.status = 'approved'
                application.user = user
                application.reviewed_by = request.user
                application.reviewed_at = timezone.now()
                application.save()
                approved_count += 1
            except Exception as e:
                self.message_user(request, f'Error approving {application.full_name}: {str(e)}', level='ERROR')
        
        self.message_user(request, f'{approved_count} application(s) approved successfully')
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        """Bulk reject applications"""
        from django.utils import timezone
        rejected_count = queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{rejected_count} application(s) rejected')
    reject_applications.short_description = 'Reject selected applications'

@admin.register(PrayerRoom)
class PrayerRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'current_topic', 'youtube_url', 'started_at', 'ended_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'current_topic', 'youtube_url')
    readonly_fields = ('is_active', 'created_at', 'updated_at', 'started_at', 'ended_at')
    fieldsets = (
        ('Prayer Room Info', {
            'fields': ('title', 'description', 'current_topic')
        }),
        ('Streaming', {
            'fields': ('youtube_url', 'is_active', 'started_at', 'ended_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['start_prayer_room', 'end_prayer_room']
    
    def has_add_permission(self, request):
        # Only allow one prayer room instance
        return not PrayerRoom.objects.exists()
        
    def start_prayer_room(self, request, queryset):
        """Admin action to start the prayer room"""
        prayer_room = PrayerRoom.get_prayer_room()
        if prayer_room.is_active:
            self.message_user(request, 'A prayer room is already active', level='error')
            return
            
        if not prayer_room.youtube_url:
            self.message_user(request, 'Please set a YouTube URL before starting', level='error')
            return
            
        prayer_room.is_active = True
        prayer_room.started_at = timezone.now()
        prayer_room.ended_at = None
        prayer_room.save()
        self.message_user(request, 'Prayer room started successfully')
    
    def end_prayer_room(self, request, queryset):
        """Admin action to end the prayer room"""
        prayer_room = PrayerRoom.get_prayer_room()
        if not prayer_room.is_active:
            self.message_user(request, 'No active prayer room to end', level='error')
            return
            
        prayer_room.is_active = False
        prayer_room.ended_at = timezone.now()
        prayer_room.save()
        self.message_user(request, 'Prayer room ended successfully')
        
    start_prayer_room.short_description = 'Start prayer room'
    end_prayer_room.short_description = 'End prayer room'

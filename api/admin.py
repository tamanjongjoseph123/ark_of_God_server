from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    User, ChurchProject, Video, InspirationQuote, 
    PrayerRequest, Testimony, UpcomingEvent, 
    Course, Module, CourseVideo, Comment, Devotion, CourseApplication, Stream, PrayerRoom
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
    list_display = ('title', 'event_status', 'event_date', 'location', 'has_youtube', 'created_at')
    list_filter = ('event_status', 'event_date', 'created_at')
    search_fields = ('title', 'description', 'location', 'youtube_url')
    
    def has_youtube(self, obj):
        return bool(obj.youtube_url)
    has_youtube.boolean = True
    has_youtube.short_description = 'Has Video'
    search_fields = ('title', 'description', 'location')
    list_filter = ('event_status', 'event_date', 'created_at')
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_status', 'location')
        }),
        ('Media & Date', {
            'fields': ('image', 'youtube_url', 'event_date')
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
    list_display = ('full_name', 'application_type', 'status', 'email', 'phone_number', 'created_at', 'get_review_status')
    list_filter = ('application_type', 'status', 'created_at', 'reviewed_at')
    search_fields = ('full_name', 'email', 'username', 'phone_number')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'password', 'reviewed_by', 'reviewed_at', 'user')
    list_editable = ('status',)
    
    fieldsets = (
        ('Application Details', {
            'fields': ('application_type', 'status')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'your_interest', 'your_goals')
        }),
        ('Account Credentials', {
            'fields': ('username', 'password'),
            'description': 'Password is hashed and cannot be viewed. For rejected applications, the user can reapply with updated information.'
        }),
        ('Review Information', {
            'fields': ('user', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_applications', 'reject_applications', 'reopen_applications']
    
    def get_review_status(self, obj):
        if obj.status == 'approved':
            return f"Approved by {obj.reviewed_by} on {obj.reviewed_at.strftime('%Y-%m-%d')}"
        elif obj.status == 'rejected':
            return f"Rejected by {obj.reviewed_by} on {obj.reviewed_at.strftime('%Y-%m-%d')}"
        return "Pending review"
    get_review_status.short_description = 'Review Status'
    
    def save_model(self, request, obj, form, change):
        # When status is changed via the admin, update the reviewed_by and reviewed_at fields
        if 'status' in form.changed_data:
            obj.reviewed_by = request.user
            from django.utils import timezone
            obj.reviewed_at = timezone.now()
            
            # If approving and no user exists, create one
            if obj.status == 'approved' and not obj.user:
                try:
                    user = User.objects.create_user(
                        username=obj.username,
                        email=obj.email,
                        password=obj.password,
                        country='',
                        contact=obj.phone_number,
                        name=obj.full_name
                    )
                    obj.user = user
                except Exception as e:
                    self.message_user(request, f'Error creating user: {str(e)}', level='ERROR')
                    return
        
        super().save_model(request, obj, form, change)
    
    def approve_applications(self, request, queryset):
        """Bulk approve applications"""
        from django.utils import timezone
        approved_count = 0
        
        for application in queryset.exclude(status='approved'):
            try:
                # If application was previously rejected and has a user, update it
                if application.status == 'rejected' and application.user:
                    user = application.user
                    user.email = application.email
                    user.contact = application.phone_number
                    user.name = application.full_name
                    user.save()
                    application.user = user
                elif not application.user:  # No user exists, create one
                    user = User.objects.create_user(
                        username=application.username,
                        email=application.email,
                        password=application.password,
                        country='',
                        contact=application.phone_number,
                        name=application.full_name
                    )
                    application.user = user
                
                application.status = 'approved'
                application.reviewed_by = request.user
                application.reviewed_at = timezone.now()
                application.save()
                approved_count += 1
            except Exception as e:
                self.message_user(request, f'Error approving {application.full_name}: {str(e)}', level='ERROR')
        
        self.message_user(request, f'{approved_count} application(s) approved successfully')
    approve_applications.short_description = 'Approve selected applications (can re-approve rejected)'
    
    def reject_applications(self, request, queryset):
        """Bulk reject applications"""
        from django.utils import timezone
        rejected_count = 0
        
        for application in queryset.exclude(status='rejected'):
            application.status = 'rejected'
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
            rejected_count += 1
        
        self.message_user(request, f'{rejected_count} application(s) rejected')
    reject_applications.short_description = 'Reject selected applications'
    
    def reopen_applications(self, request, queryset):
        """Reopen rejected applications to allow reapplication"""
        from django.utils import timezone
        reopened_count = 0
        
        for application in queryset.filter(status='rejected'):
            # Create a new application with the same details but new timestamps
            try:
                new_application = CourseApplication.objects.create(
                    application_type=application.application_type,
                    full_name=application.full_name,
                    email=application.email,
                    phone_number=application.phone_number,
                    your_interest=application.your_interest,
                    your_goals=application.your_goals,
                    username=application.username,
                    password=application.password,
                    status='pending',
                    # Reset review fields
                    reviewed_by=None,
                    reviewed_at=None,
                    # Keep the user reference for tracking
                    user=application.user
                )
                reopened_count += 1
            except Exception as e:
                self.message_user(request, f'Error reopening {application.full_name}: {str(e)}', level='ERROR')
        
        self.message_user(request, f'{reopened_count} application(s) reopened for reapplication')
    reopen_applications.short_description = 'Reopen selected rejected applications for reapplication'

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'scheduled_time', 'created_at', 'stream_preview')
    list_filter = ('scheduled_time',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'stream_preview')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'stream_url', 'thumbnail_url', 'scheduled_time')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'stream_preview'),
            'classes': ('collapse',)
        }),
    )
    actions = ['delete_selected', 'clear_old_streams']
    
    def has_add_permission(self, request):
        # Don't allow adding new streams if one already exists
        return not Stream.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Allow admins to delete the stream
        return True
    
    def get_actions(self, request):
        # Only allow delete_selected action
        actions = super().get_actions(request)
        return {k: v for k, v in actions.items() if k in ['delete_selected']}
    
    def get_queryset(self, request):
        # Only show the single stream
        qs = super().get_queryset(request)
        # Get the first stream or return an empty queryset if none exists
        stream = qs.first()
        return qs.filter(pk=stream.pk) if stream else qs.none()
    
    def changelist_view(self, request, extra_context=None):
        # If no stream exists, create one
        if not Stream.objects.exists():
            Stream.objects.create(
                title='Live Stream',
                stream_url='https://www.youtube.com/'
            )
        return super().changelist_view(request, extra_context)
    
    def stream_preview(self, obj):
        if not obj.stream_url:
            return "No stream URL provided"
            
        if 'youtube.com' in obj.stream_url or 'youtu.be' in obj.stream_url:
            video_id = None
            if 'youtube.com/watch?v=' in obj.stream_url:
                video_id = obj.stream_url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in obj.stream_url:
                video_id = obj.stream_url.split('youtu.be/')[-1].split('?')[0]
                
            if video_id:
                return format_html(
                    '<div style="margin: 10px 0;">'\
                    '<div style="max-width: 560px; margin: 0 auto;">'\
                    '<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">'\
                    f'<iframe width="100%" height="100%" '
                    'style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" '
                    f'src="https://www.youtube.com/embed/{video_id}?rel=0" '
                    'frameborder="0" '
                    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
                    'allowfullscreen></iframe>'\
                    '</div></div></div>',
                    video_id
                )
        
        # For other platforms, just show a link
        return format_html(f'<a href="{obj.stream_url}" target="_blank" class="button">View Stream</a>')
    
    stream_preview.short_description = 'Live Preview'
    
    @admin.action(description='Clear old streams')
    def clear_old_streams(self, request, queryset):
        """Remove old streams that are not scheduled for the future."""
        cutoff = timezone.now() - timezone.timedelta(days=30)
        old_streams = Stream.objects.filter(
            scheduled_time__lt=timezone.now(),
            created_at__lt=cutoff
        )
        count = old_streams.count()
        old_streams.delete()
        self.message_user(request, f'Removed {count} old streams')
    clear_old_streams.short_description = 'Remove old streams (older than 30 days)'

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

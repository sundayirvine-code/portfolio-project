from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, LoginAttempt, UserSession, UserActivity


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('bio', 'location', 'website', 'profile_image_base64')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Professional Info', {
            'fields': ('job_title', 'company', 'experience_years'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'marketing_emails'),
            'classes': ('collapse',)
        }),
    )


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline"""
    inlines = (UserProfileInline,)
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login_display')
    list_filter = BaseUserAdmin.list_filter + ('profile__email_notifications',)
    
    def last_login_display(self, obj):
        if obj.last_login:
            return obj.last_login.strftime('%Y-%m-%d %H:%M')
        return 'Never'
    last_login_display.short_description = 'Last Login'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model"""
    list_display = ('user', 'job_title', 'company', 'location', 'created_at', 'profile_image_preview')
    list_filter = ('email_notifications', 'marketing_emails', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'job_title', 'company')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'location', 'website', 'profile_image_base64')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Professional Information', {
            'fields': ('job_title', 'company', 'experience_years'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'marketing_emails'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def profile_image_preview(self, obj):
        if obj.profile_image_base64:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_image_base64
            )
        return 'No Image'
    profile_image_preview.short_description = 'Profile Image'


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Admin for LoginAttempt model"""
    list_display = ('username', 'ip_address', 'success', 'timestamp', 'success_badge')
    list_filter = ('success', 'timestamp')
    search_fields = ('username', 'ip_address')
    readonly_fields = ('username', 'ip_address', 'user_agent', 'success', 'timestamp', 'session_key', 'location_info')
    date_hierarchy = 'timestamp'
    
    def success_badge(self, obj):
        if obj.success:
            return format_html('<span style="color: green;">✓ Success</span>')
        return format_html('<span style="color: red;">✗ Failed</span>')
    success_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Don't allow manual creation
    
    def has_change_permission(self, request, obj=None):
        return False  # Read-only
    
    actions = ['mark_as_reviewed']
    
    def mark_as_reviewed(self, request, queryset):
        # This could be used to mark suspicious attempts as reviewed
        pass
    mark_as_reviewed.short_description = "Mark selected attempts as reviewed"


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin for UserSession model"""
    list_display = ('user', 'ip_address', 'created_at', 'last_activity', 'is_active', 'session_status')
    list_filter = ('is_active', 'created_at', 'last_activity')
    search_fields = ('user__username', 'ip_address', 'session_key')
    readonly_fields = ('user', 'session_key', 'ip_address', 'user_agent', 'created_at', 'last_activity', 'location_info')
    date_hierarchy = 'created_at'
    
    def session_status(self, obj):
        if obj.is_current_session:
            return format_html('<span style="color: green;">🟢 Active</span>')
        return format_html('<span style="color: orange;">🟡 Expired</span>')
    session_status.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can modify
    
    actions = ['deactivate_sessions']
    
    def deactivate_sessions(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {queryset.count()} sessions.")
    deactivate_sessions.short_description = "Deactivate selected sessions"


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin for UserActivity model"""
    list_display = ('user_display', 'action', 'description', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'action', 'description', 'ip_address', 'user_agent', 'referer', 'metadata', 'timestamp')
    date_hierarchy = 'timestamp'
    
    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return 'Anonymous'
    user_display.short_description = 'User'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    # Custom admin views for analytics
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Add some basic analytics
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        
        extra_context['today_activities'] = UserActivity.objects.filter(timestamp__date=today).count()
        extra_context['week_activities'] = UserActivity.objects.filter(timestamp__gte=week_ago).count()
        extra_context['total_activities'] = UserActivity.objects.count()
        
        # Most common actions this week
        from django.db.models import Count
        common_actions = UserActivity.objects.filter(
            timestamp__gte=week_ago
        ).values('action').annotate(
            count=Count('action')
        ).order_by('-count')[:5]
        
        extra_context['common_actions'] = common_actions
        
        return super().changelist_view(request, extra_context)


# Re-register User admin with our custom admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile Information
    bio = models.TextField(max_length=1000, blank=True, help_text="Brief biography")
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Profile Image (Base64)
    profile_image_base64 = models.TextField(
        blank=True,
        help_text="Profile image as base64 encoded string"
    )
    
    # Social Links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Professional Information
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    
    # Contact Preferences
    email_notifications = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
    
    @property
    def display_name(self):
        """Return the best available display name"""
        return self.user.get_full_name() or self.user.username
    
    @property
    def profile_image_url(self):
        """Return profile image URL or placeholder"""
        if self.profile_image_base64:
            return self.profile_image_base64
        return None


class LoginAttempt(models.Model):
    """Track login attempts for security monitoring"""
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional security fields
    session_key = models.CharField(max_length=40, blank=True)
    location_info = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'login_attempts'
        verbose_name = 'Login Attempt'
        verbose_name_plural = 'Login Attempts'
        ordering = ['-timestamp']
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.username} - {status} - {self.timestamp}"


class UserSession(models.Model):
    """Track active user sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Session metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Location info (optional)
    location_info = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.created_at}"
    
    @property
    def is_current_session(self):
        """Check if session is still active"""
        timeout_minutes = 30
        timeout_threshold = timezone.now() - timezone.timedelta(minutes=timeout_minutes)
        return self.last_activity > timeout_threshold and self.is_active


class UserActivity(models.Model):
    """Track user activities for analytics"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('contact_form', 'Contact Form Submission'),
        ('project_view', 'Project View'),
        ('blog_view', 'Blog Post View'),
        ('search', 'Search'),
        ('download', 'File Download'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='activities',
        null=True, 
        blank=True  # Allow anonymous activities
    )
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    
    # Request metadata
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referer = models.URLField(blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['ip_address', '-timestamp']),
        ]
    
    def __str__(self):
        user_display = self.user.username if self.user else 'Anonymous'
        return f"{user_display} - {self.get_action_display()} - {self.timestamp}"


# Signal handlers to create UserProfile automatically
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
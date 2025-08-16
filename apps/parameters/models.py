from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


class SiteParameter(models.Model):
    """Model for site-wide configuration parameters"""
    
    THEME_CHOICES = [
        ('electric_neon', 'Electric Neon (Tech-Forward)'),
        ('sunset_gradient', 'Sunset Gradient (Creative)'),
        ('ocean_deep', 'Ocean Deep (Professional)'),
        ('forest_modern', 'Forest Modern (Eco-Friendly)'),
    ]
    
    MODE_CHOICES = [
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
        ('auto', 'Auto (System Preference)'),
    ]
    
    # Site Information
    site_name = models.CharField(_("Site Name"), max_length=100, default="Portfolio")
    site_tagline = models.CharField(_("Site Tagline"), max_length=200, blank=True)
    site_description = models.TextField(_("Site Description"), blank=True)
    site_url = models.URLField(_("Site URL"), blank=True)
    
    # Theme Settings
    active_theme = models.CharField(
        _("Active Theme"), 
        max_length=20, 
        choices=THEME_CHOICES, 
        default='electric_neon'
    )
    default_mode = models.CharField(
        _("Default Mode"), 
        max_length=10, 
        choices=MODE_CHOICES, 
        default='auto'
    )
    
    # Contact Information
    email = models.EmailField(_("Contact Email"), blank=True)
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    
    # SEO Settings
    meta_title = models.CharField(_("Meta Title"), max_length=60, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)
    meta_keywords = models.CharField(_("Meta Keywords"), max_length=255, blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(_("Google Analytics ID"), max_length=20, blank=True)
    
    # Social Media Links
    github_url = models.URLField(_("GitHub URL"), blank=True)
    linkedin_url = models.URLField(_("LinkedIn URL"), blank=True)
    twitter_url = models.URLField(_("Twitter URL"), blank=True)
    instagram_url = models.URLField(_("Instagram URL"), blank=True)
    
    # Feature Flags
    enable_blog = models.BooleanField(_("Enable Blog"), default=True)
    enable_testimonials = models.BooleanField(_("Enable Testimonials"), default=True)
    enable_contact_form = models.BooleanField(_("Enable Contact Form"), default=True)
    enable_animations = models.BooleanField(_("Enable Animations"), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Site Parameter")
        verbose_name_plural = _("Site Parameters")
    
    def __str__(self):
        return f"{self.site_name} Settings"
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings


class NavigationMenu(models.Model):
    """Model for navigation menu items"""
    
    title = models.CharField(_("Menu Title"), max_length=50)
    url = models.CharField(_("URL"), max_length=200)
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True, help_text="Bootstrap or Font Awesome icon class")
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_external = models.BooleanField(_("Is External Link"), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Navigation Menu Item")
        verbose_name_plural = _("Navigation Menu Items")
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class ColorPalette(models.Model):
    """Model for custom color palettes"""
    
    name = models.CharField(_("Palette Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Slug"), unique=True)
    
    # Light Mode Colors
    light_primary = models.CharField(_("Light Primary Color"), max_length=7, default="#6366f1")
    light_secondary = models.CharField(_("Light Secondary Color"), max_length=7, default="#8b5cf6")
    light_accent = models.CharField(_("Light Accent Color"), max_length=7, default="#06b6d4")
    light_background = models.CharField(_("Light Background Color"), max_length=7, default="#f8fafc")
    light_text = models.CharField(_("Light Text Color"), max_length=7, default="#1e293b")
    
    # Dark Mode Colors
    dark_primary = models.CharField(_("Dark Primary Color"), max_length=7, default="#818cf8")
    dark_secondary = models.CharField(_("Dark Secondary Color"), max_length=7, default="#a78bfa")
    dark_accent = models.CharField(_("Dark Accent Color"), max_length=7, default="#67e8f9")
    dark_background = models.CharField(_("Dark Background Color"), max_length=7, default="#0f172a")
    dark_text = models.CharField(_("Dark Text Color"), max_length=7, default="#f1f5f9")
    
    # Additional Settings
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_default = models.BooleanField(_("Is Default"), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Color Palette")
        verbose_name_plural = _("Color Palettes")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Ensure only one default palette exists"""
        if self.is_default:
            ColorPalette.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

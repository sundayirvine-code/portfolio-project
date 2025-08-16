from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
import json


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
    
    FONT_PALETTE_CHOICES = [
        ('modern_professional', 'Modern Professional'),
        ('creative_editorial', 'Creative Editorial'),
        ('tech_minimalist', 'Tech Minimalist'),
        ('warm_humanist', 'Warm Humanist'),
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
    active_font_palette = models.CharField(
        _("Active Font Palette"),
        max_length=20,
        choices=FONT_PALETTE_CHOICES,
        default='modern_professional'
    )
    
    # Contact Information
    email = models.EmailField(_("Contact Email"), blank=True)
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    
    # Owner Information
    owner_name = models.CharField(_("Owner Full Name"), max_length=100, blank=True)
    owner_title = models.CharField(_("Professional Title"), max_length=200, blank=True)
    profile_image_base64 = models.TextField(_("Profile Image (Base64)"), blank=True)
    
    # Dynamic About Content
    about_me_text = models.TextField(_("About Me Text"), blank=True, 
                                   help_text="Main about section content")
    my_story_text = models.TextField(_("My Story Text"), blank=True,
                                   help_text="Personal/professional story content")
    bio = models.TextField(_("Bio"), blank=True, help_text="Short biography")
    
    # Values and Interests (stored as JSON)
    values_interests = models.JSONField(_("Values & Interests"), default=dict, blank=True,
                                      help_text="Store as JSON: {'values': [...], 'interests': [...]}")
    
    # Fun Facts (stored as JSON)
    fun_facts = models.JSONField(_("Fun Facts"), default=dict, blank=True,
                               help_text="Store as JSON: {'cups_of_coffee': 500, 'projects_completed': 50, ...}")
    
    # Contact Section Dynamic Content
    availability_status = models.CharField(_("Availability Status"), max_length=20,
                                         choices=[
                                             ('available', 'Available for Projects'),
                                             ('busy', 'Currently Busy'),
                                             ('unavailable', 'Not Available'),
                                         ], default='available')
    availability_message = models.TextField(_("Availability Message"), blank=True,
                                          help_text="Custom message about availability")
    response_time = models.CharField(_("Response Time"), max_length=50, 
                                   default="Usually within 24 hours")
    
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


class FontPalette(models.Model):
    """Model for custom font palettes"""
    
    name = models.CharField(_("Palette Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"), blank=True)
    
    # Font Family Definitions
    heading_font = models.CharField(_("Heading Font"), max_length=200,
                                  help_text="CSS font-family for headings")
    body_font = models.CharField(_("Body Font"), max_length=200,
                               help_text="CSS font-family for body text")
    accent_font = models.CharField(_("Accent Font"), max_length=200, blank=True,
                                 help_text="CSS font-family for accents/special elements")
    
    # Font Weights and Sizes
    heading_weight = models.CharField(_("Heading Font Weight"), max_length=10, default="700")
    body_weight = models.CharField(_("Body Font Weight"), max_length=10, default="400")
    base_font_size = models.CharField(_("Base Font Size"), max_length=10, default="16px")
    
    # Google Fonts URLs (if needed)
    google_fonts_url = models.URLField(_("Google Fonts URL"), blank=True,
                                     help_text="URL to import Google Fonts")
    
    # Settings
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_default = models.BooleanField(_("Is Default"), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Font Palette")
        verbose_name_plural = _("Font Palettes")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Ensure only one default palette exists"""
        if self.is_default:
            FontPalette.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class ProfessionalJourney(models.Model):
    """Model for professional experience timeline"""
    
    ENTRY_TYPE_CHOICES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
        ('certification', 'Certification'),
        ('achievement', 'Achievement'),
        ('project', 'Major Project'),
    ]
    
    title = models.CharField(_("Title/Position"), max_length=200)
    company = models.CharField(_("Company/Institution"), max_length=200)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), null=True, blank=True,
                              help_text="Leave blank if current position")
    is_current = models.BooleanField(_("Is Current Position"), default=False)
    
    description = models.TextField(_("Description"))
    achievements = models.TextField(_("Key Achievements"), blank=True,
                                  help_text="Bullet points of achievements")
    technologies = models.TextField(_("Technologies Used"), blank=True,
                                  help_text="Comma-separated list of technologies")
    
    entry_type = models.CharField(_("Entry Type"), max_length=20,
                                choices=ENTRY_TYPE_CHOICES, default='work')
    
    # Ordering and visibility
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_featured = models.BooleanField(_("Is Featured"), default=False,
                                    help_text="Show in featured experience section")
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Professional Journey Entry")
        verbose_name_plural = _("Professional Journey Entries")
        ordering = ['-start_date', 'order']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def duration(self):
        """Calculate duration of experience"""
        from datetime import date
        end = self.end_date or date.today()
        start = self.start_date
        
        years = end.year - start.year
        months = end.month - start.month
        
        if months < 0:
            years -= 1
            months += 12
        
        if years > 0 and months > 0:
            return f"{years} year{'s' if years > 1 else ''}, {months} month{'s' if months > 1 else ''}"
        elif years > 0:
            return f"{years} year{'s' if years > 1 else ''}"
        elif months > 0:
            return f"{months} month{'s' if months > 1 else ''}"
        else:
            return "Less than a month"
    
    @property
    def achievements_list(self):
        """Return achievements as a list"""
        if self.achievements:
            return [item.strip() for item in self.achievements.split('\n') if item.strip()]
        return []
    
    @property
    def technologies_list(self):
        """Return technologies as a list"""
        if self.technologies:
            return [item.strip() for item in self.technologies.split(',') if item.strip()]
        return []


class FAQ(models.Model):
    """Model for Frequently Asked Questions"""
    
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('services', 'Services'),
        ('process', 'Process'),
        ('pricing', 'Pricing'),
        ('technical', 'Technical'),
        ('contact', 'Contact'),
    ]
    
    question = models.CharField(_("Question"), max_length=300)
    answer = models.TextField(_("Answer"))
    category = models.CharField(_("Category"), max_length=20,
                              choices=CATEGORY_CHOICES, default='general')
    
    # Ordering and visibility
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_featured = models.BooleanField(_("Is Featured"), default=False,
                                    help_text="Show in main FAQ section")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['category', 'order', 'question']
    
    def __str__(self):
        return self.question


class QuickAnswer(models.Model):
    """Model for quick answers in contact section"""
    
    question = models.CharField(_("Question"), max_length=200)
    answer = models.TextField(_("Answer"), max_length=500)
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True,
                          help_text="Bootstrap icon class (e.g., bi-clock)")
    
    # Ordering and visibility
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Quick Answer")
        verbose_name_plural = _("Quick Answers")
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question

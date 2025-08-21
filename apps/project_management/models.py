from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_image_file_extension
import base64
import io
from PIL import Image


class Category(models.Model):
    """Category model for projects and blog posts"""
    
    name = models.CharField(_("Category Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    color = models.CharField(_("Color"), max_length=7, default="#6366f1", help_text="Hex color code")
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Technology(models.Model):
    """Technology/Skill model"""
    
    name = models.CharField(_("Technology Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True)
    website_url = models.URLField(_("Official Website"), blank=True)
    proficiency = models.PositiveIntegerField(
        _("Proficiency Level"), 
        default=50, 
        help_text="Proficiency level from 0 to 100"
    )
    years_experience = models.DecimalField(
        _("Years of Experience"), 
        max_digits=4, 
        decimal_places=1, 
        default=0.0
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Technology")
        verbose_name_plural = _("Technologies")
        ordering = ['-proficiency', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Project portfolio model"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('featured', _('Featured')),
        ('archived', _('Archived')),
    ]
    
    TYPE_CHOICES = [
        ('web_app', _('Web Application')),
        ('mobile_app', _('Mobile Application')),
        ('desktop_app', _('Desktop Application')),
        ('api', _('API/Backend')),
        ('website', _('Website')),
        ('other', _('Other')),
    ]
    
    # Basic Information
    title = models.CharField(_("Project Title"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Short Description"))
    detailed_description = models.TextField(_("Detailed Description"), blank=True)
    
    # Project Details
    project_type = models.CharField(_("Project Type"), max_length=20, choices=TYPE_CHOICES, default='web_app')
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    
    # Media
    featured_image = models.TextField(_("Featured Image"), blank=True, help_text="Base64 encoded image data")
    gallery_images = models.TextField(_("Gallery Images"), blank=True, help_text="JSON array of base64 encoded images")
    
    # Links
    live_url = models.URLField(_("Live Demo URL"), blank=True)
    github_url = models.URLField(_("GitHub Repository"), blank=True)
    documentation_url = models.URLField(_("Documentation URL"), blank=True)
    
    # Metadata
    start_date = models.DateField(_("Start Date"), blank=True, null=True)
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    client = models.CharField(_("Client/Company"), max_length=100, blank=True)
    team_size = models.PositiveIntegerField(_("Team Size"), default=1)
    
    # Project Content Details
    key_features = models.TextField(_("Key Features"), blank=True, help_text="JSON array of key features")
    challenges = models.TextField(_("Challenges"), blank=True, help_text="Description of challenges faced")
    solutions = models.TextField(_("Solutions"), blank=True, help_text="How challenges were solved")
    results = models.TextField(_("Results & Impact"), blank=True, help_text="Project outcomes and impact")
    
    # SEO
    meta_title = models.CharField(_("Meta Title"), max_length=60, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status in ['published', 'featured']
    
    @property
    def duration_months(self):
        if self.start_date and self.end_date:
            return (self.end_date.year - self.start_date.year) * 12 + (self.end_date.month - self.start_date.month)
        return None
    
    @property
    def featured_image_url(self):
        """Get data URL for featured image"""
        if self.featured_image and self.featured_image.startswith('data:image'):
            return self.featured_image
        elif self.featured_image:
            return f"data:image/jpeg;base64,{self.featured_image}"
        return None
    
    def set_featured_image_from_file(self, image_file):
        """Convert uploaded image file to base64"""
        if image_file:
            # Open and resize image if needed
            img = Image.open(image_file)
            
            # Resize to max 1200px width while maintaining aspect ratio
            if img.width > 1200:
                ratio = 1200 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Save to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            img_bytes = buffer.getvalue()
            
            # Encode to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            self.featured_image = f"data:image/jpeg;base64,{img_base64}"
    
    @property
    def gallery_images_list(self):
        """Get list of gallery image data URLs"""
        if self.gallery_images:
            try:
                import json
                images = json.loads(self.gallery_images)
                return [img if img.startswith('data:image') else f"data:image/jpeg;base64,{img}" for img in images]
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    @property
    def key_features_list(self):
        """Get list of key features from JSON"""
        if self.key_features:
            try:
                import json
                return json.loads(self.key_features)
            except (json.JSONDecodeError, TypeError):
                return []
        return []


class BlogPost(models.Model):
    """Blog post model"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('featured', _('Featured')),
    ]
    
    # Basic Information
    title = models.CharField(_("Post Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, max_length=200)
    excerpt = models.TextField(_("Excerpt"), max_length=300, blank=True)
    content = models.TextField(_("Content"))
    
    # Metadata
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(_("Tags"), max_length=200, blank=True, help_text="Comma-separated tags")
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Media
    featured_image = models.TextField(_("Featured Image"), blank=True, help_text="Base64 encoded image data")
    
    # SEO
    meta_title = models.CharField(_("Meta Title"), max_length=60, blank=True)
    meta_description = models.CharField(_("Meta Description"), max_length=160, blank=True)
    
    # Statistics
    views_count = models.PositiveIntegerField(_("Views Count"), default=0)
    reading_time = models.PositiveIntegerField(_("Reading Time (minutes)"), default=0, help_text="Estimated reading time in minutes")
    
    # Timestamps
    published_at = models.DateTimeField(_("Published At"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status in ['published', 'featured']
    
    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    @property
    def featured_image_url(self):
        """Get data URL for featured image"""
        if self.featured_image and self.featured_image.startswith('data:image'):
            return self.featured_image
        elif self.featured_image:
            return f"data:image/jpeg;base64,{self.featured_image}"
        return None
    
    def set_featured_image_from_file(self, image_file):
        """Convert uploaded image file to base64"""
        if image_file:
            # Open and resize image if needed
            img = Image.open(image_file)
            
            # Resize to max 800px width while maintaining aspect ratio
            if img.width > 800:
                ratio = 800 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((800, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Save to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            img_bytes = buffer.getvalue()
            
            # Encode to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            self.featured_image = f"data:image/jpeg;base64,{img_base64}"


class Testimonial(models.Model):
    """Client testimonial model"""
    
    # Client Information
    client_name = models.CharField(_("Client Name"), max_length=100)
    client_position = models.CharField(_("Position/Title"), max_length=100, blank=True)
    client_company = models.CharField(_("Company"), max_length=100, blank=True)
    client_email = models.EmailField(_("Client Email"), blank=True)
    client_photo = models.TextField(_("Client Photo"), blank=True, help_text="Base64 encoded image data")
    
    # Testimonial Content
    content = models.TextField(_("Testimonial Content"))
    rating = models.PositiveIntegerField(
        _("Rating"), 
        default=5, 
        help_text="Rating from 1 to 5 stars"
    )
    
    # Related Project
    project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='testimonials'
    )
    
    # Settings
    is_featured = models.BooleanField(_("Is Featured"), default=False)
    is_approved = models.BooleanField(_("Is Approved"), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Testimonial from {self.client_name}"
    
    @property
    def client_photo_url(self):
        """Get data URL for client photo"""
        if self.client_photo and self.client_photo.startswith('data:image'):
            return self.client_photo
        elif self.client_photo:
            return f"data:image/jpeg;base64,{self.client_photo}"
        return None
    
    def set_client_photo_from_file(self, image_file):
        """Convert uploaded image file to base64"""
        if image_file:
            # Open and resize image if needed
            img = Image.open(image_file)
            
            # Resize to 200x200 square
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Save to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            img_bytes = buffer.getvalue()
            
            # Encode to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            self.client_photo = f"data:image/jpeg;base64,{img_base64}"


class Service(models.Model):
    """Service/Skill offering model"""
    
    # Basic Information
    name = models.CharField(_("Service Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"))
    short_description = models.CharField(_("Short Description"), max_length=200, blank=True)
    
    # Details
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    delivery_time = models.CharField(_("Delivery Time"), max_length=50, blank=True, help_text="e.g., '2-4 weeks'")
    features = models.TextField(_("Key Features"), blank=True, help_text="JSON array of key features")
    process_steps = models.TextField(_("Process Steps"), blank=True, help_text="JSON array of process steps")
    
    # Pricing (optional)
    starting_price = models.DecimalField(
        _("Starting Price"), 
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    price_unit = models.CharField(
        _("Price Unit"), 
        max_length=20, 
        default="per project",
        blank=True
    )
    
    # Settings
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_featured = models.BooleanField(_("Is Featured"), default=False)
    order = models.PositiveIntegerField(_("Display Order"), default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def features_list(self):
        """Get list of features from JSON"""
        if self.features:
            try:
                import json
                return json.loads(self.features)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    @property
    def process_steps_list(self):
        """Get list of process steps from JSON"""
        if self.process_steps:
            try:
                import json
                return json.loads(self.process_steps)
            except (json.JSONDecodeError, TypeError):
                return []
        return []


class ContactMessage(models.Model):
    """Contact form submission model"""
    
    STATUS_CHOICES = [
        ('new', _('New')),
        ('in_progress', _('In Progress')),
        ('replied', _('Replied')),
        ('closed', _('Closed')),
    ]
    
    # Contact Information
    name = models.CharField(_("Full Name"), max_length=100)
    email = models.EmailField(_("Email Address"))
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    company = models.CharField(_("Company"), max_length=100, blank=True)
    
    # Message Details
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))
    service_interest = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_("Service of Interest")
    )
    
    # Metadata
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(_("IP Address"), blank=True, null=True)
    user_agent = models.TextField(_("User Agent"), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

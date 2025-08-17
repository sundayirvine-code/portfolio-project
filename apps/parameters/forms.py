from django import forms
from django.core.validators import RegexValidator
from django.forms import formset_factory
import json
from .models import SiteParameter, NavigationMenu, ColorPalette, FontPalette, ProfessionalJourney, FAQ, QuickAnswer


class SiteParameterForm(forms.ModelForm):
    """Form for managing site parameters"""
    
    class Meta:
        model = SiteParameter
        fields = [
            'site_name', 'site_tagline', 'site_description', 'site_url',
            'active_theme', 'default_mode',
            'email', 'phone', 'location',
            'meta_title', 'meta_description', 'meta_keywords',
            'google_analytics_id',
            'github_url', 'linkedin_url', 'twitter_url', 'instagram_url',
            'enable_blog', 'enable_testimonials', 'enable_contact_form', 'enable_animations'
        ]
        
        widgets = {
            'site_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Portfolio Name'
            }),
            'site_tagline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief tagline about your work'
            }),
            'site_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your portfolio and services'
            }),
            'site_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com'
            }),
            'active_theme': forms.Select(attrs={'class': 'form-select'}),
            'default_mode': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (60 chars max)',
                'maxlength': 60
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (160 chars max)',
                'maxlength': 160
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'keyword1, keyword2, keyword3'
            }),
            'google_analytics_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'G-XXXXXXXXXX'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/yourusername'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/yourusername'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/yourusername'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/yourusername'
            }),
            'enable_blog': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_testimonials': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_contact_form': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_animations': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add help text
        self.fields['meta_title'].help_text = "Optimal length: 50-60 characters"
        self.fields['meta_description'].help_text = "Optimal length: 150-160 characters"
        self.fields['google_analytics_id'].help_text = "Format: G-XXXXXXXXXX"
        
    def clean_google_analytics_id(self):
        """Validate Google Analytics ID format"""
        ga_id = self.cleaned_data.get('google_analytics_id')
        if ga_id and not ga_id.startswith('G-'):
            raise forms.ValidationError("Google Analytics ID must start with 'G-'")
        return ga_id


class NavigationMenuForm(forms.ModelForm):
    """Form for managing navigation menu items"""
    
    class Meta:
        model = NavigationMenu
        fields = ['title', 'url', 'icon', 'order', 'is_active', 'is_external']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Menu Title'
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/path/ or https://external.com'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'bi bi-house or fas fa-home'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_external': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add help text
        self.fields['icon'].help_text = "Bootstrap Icons (bi bi-house) or Font Awesome (fas fa-home)"
        self.fields['url'].help_text = "Internal path (/about/) or external URL (https://...)"
        self.fields['order'].help_text = "Lower numbers appear first in navigation"
        self.fields['is_external'].help_text = "Check if this link goes to an external website"
    
    def clean_url(self):
        """Validate URL format"""
        url = self.cleaned_data.get('url')
        is_external = self.cleaned_data.get('is_external', False)
        
        if not url:
            raise forms.ValidationError("URL is required")
        
        if is_external and not (url.startswith('http://') or url.startswith('https://')):
            raise forms.ValidationError("External URLs must start with http:// or https://")
        
        if not is_external and not url.startswith('/'):
            raise forms.ValidationError("Internal URLs must start with /")
        
        return url


class ColorPaletteForm(forms.ModelForm):
    """Form for managing color palettes"""
    
    # Color field validator
    color_validator = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message='Enter a valid hex color code (e.g., #FF0000 or #F00)'
    )
    
    class Meta:
        model = ColorPalette
        fields = [
            'name', 'slug',
            'light_primary', 'light_secondary', 'light_accent', 'light_background', 'light_text',
            'dark_primary', 'dark_secondary', 'dark_accent', 'dark_background', 'dark_text',
            'is_active', 'is_default'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Palette Name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'palette-slug'
            }),
            'light_primary': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'light_secondary': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'light_accent': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'light_background': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'light_text': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'dark_primary': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'dark_secondary': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'dark_accent': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'dark_background': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'dark_text': forms.TextInput(attrs={
                'class': 'form-control color-picker',
                'type': 'color'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add validators to color fields
        color_fields = [
            'light_primary', 'light_secondary', 'light_accent', 'light_background', 'light_text',
            'dark_primary', 'dark_secondary', 'dark_accent', 'dark_background', 'dark_text'
        ]
        
        for field_name in color_fields:
            self.fields[field_name].validators.append(self.color_validator)
        
        # Add help text
        self.fields['slug'].help_text = "URL-friendly version of the name (auto-generated if empty)"
        self.fields['is_default'].help_text = "Only one palette can be set as default"
    
    def clean_slug(self):
        """Auto-generate slug if not provided"""
        slug = self.cleaned_data.get('slug')
        name = self.cleaned_data.get('name')
        
        if not slug and name:
            from django.utils.text import slugify
            slug = slugify(name)
        
        # Check for uniqueness
        if slug:
            existing = ColorPalette.objects.filter(slug=slug)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError("A palette with this slug already exists.")
        
        return slug
    
    def clean(self):
        """Custom validation for the entire form"""
        cleaned_data = super().clean()
        
        # Validate color contrast (basic check)
        light_bg = cleaned_data.get('light_background')
        light_text = cleaned_data.get('light_text')
        dark_bg = cleaned_data.get('dark_background')
        dark_text = cleaned_data.get('dark_text')
        
        # Add more sophisticated color contrast validation here if needed
        
        return cleaned_data


class ExtendedSiteParameterForm(forms.ModelForm):
    """Extended form for managing all site parameters including JSON fields"""
    
    class Meta:
        model = SiteParameter
        fields = [
            # Basic Site Information
            'site_name', 'site_tagline', 'site_description', 'site_url',
            # Owner Information  
            'owner_name', 'owner_title', 'profile_image_base64',
            # Theme Settings
            'active_theme', 'default_mode', 'active_font_palette',
            # Typography Settings
            'base_font_size', 'heading_font_scale', 'small_font_scale',
            # Contact Information
            'email', 'phone', 'location',
            # Dynamic Content
            'about_me_text', 'my_story_text', 'bio',
            # Availability
            'availability_status', 'availability_message', 'response_time',
            # SEO Settings
            'meta_title', 'meta_description', 'meta_keywords',
            # Analytics
            'google_analytics_id',
            # Social Media
            'github_url', 'linkedin_url', 'twitter_url', 'instagram_url',
            # Feature Flags
            'enable_blog', 'enable_testimonials', 'enable_contact_form', 'enable_animations',
        ]
        
        widgets = {
            # Basic Information
            'site_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Portfolio Name'}),
            'site_tagline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief tagline about your work'}),
            'site_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your portfolio'}),
            'site_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourportfolio.com'}),
            
            # Owner Information
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'owner_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Professional Title'}),
            'profile_image_base64': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Base64 encoded image data'}),
            
            # Theme Settings
            'active_theme': forms.Select(attrs={'class': 'form-select'}),
            'default_mode': forms.Select(attrs={'class': 'form-select'}),
            'active_font_palette': forms.Select(attrs={'class': 'form-select'}),
            
            # Typography
            'base_font_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '16px'}),
            'heading_font_scale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1.0'}),
            'small_font_scale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.5'}),
            
            # Contact Information
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            
            # Dynamic Content
            'about_me_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell visitors about yourself'}),
            'my_story_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your professional story'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short biography'}),
            
            # Availability
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
            'availability_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Custom availability message'}),
            'response_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usually within 24 hours'}),
            
            # SEO
            'meta_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SEO title (60 chars max)', 'maxlength': 60}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SEO description (160 chars max)', 'maxlength': 160}),
            'meta_keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'keyword1, keyword2, keyword3'}),
            
            # Analytics
            'google_analytics_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'G-XXXXXXXXXX'}),
            
            # Social Media
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/yourusername'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourusername'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourusername'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourusername'}),
            
            # Feature Flags
            'enable_blog': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_testimonials': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_contact_form': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_animations': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FontPaletteForm(forms.ModelForm):
    """Form for managing font palettes"""
    
    class Meta:
        model = FontPalette
        fields = [
            'name', 'slug', 'description',
            'heading_font', 'body_font', 'accent_font',
            'heading_weight', 'body_weight', 'base_font_size',
            'google_fonts_url', 'is_active', 'is_default'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Font Palette Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'font-palette-slug'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Brief description'}),
            'heading_font': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "'Inter', sans-serif"}),
            'body_font': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "'Inter', sans-serif"}),
            'accent_font': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "'Inter', sans-serif"}),
            'heading_weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '700'}),
            'body_weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '400'}),
            'base_font_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '16px'}),
            'google_fonts_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://fonts.googleapis.com/css2?family=Inter'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProfessionalJourneyForm(forms.ModelForm):
    """Form for managing professional journey entries"""
    
    class Meta:
        model = ProfessionalJourney
        fields = [
            'title', 'company', 'location', 'entry_type',
            'start_date', 'end_date', 'is_current',
            'description', 'achievements', 'technologies',
            'order', 'is_featured', 'is_active'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title / Degree Name'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company / Institution'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'entry_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description'}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'One achievement per line'}),
            'technologies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Comma-separated technologies'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FAQForm(forms.ModelForm):
    """Form for managing FAQ entries"""
    
    class Meta:
        model = FAQ
        fields = [
            'question', 'answer', 'category',
            'order', 'is_featured', 'is_active'
        ]
        
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What is your question?'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide a detailed answer'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuickAnswerForm(forms.ModelForm):
    """Form for managing quick answers"""
    
    class Meta:
        model = QuickAnswer
        fields = [
            'question', 'answer', 'icon',
            'order', 'is_active'
        ]
        
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quick question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief answer'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'bi-clock'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
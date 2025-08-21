"""
Admin forms for project management models
Comprehensive forms for CRUD operations with validation and image handling
"""

from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext_lazy as _
from .models import Category, Technology, Project, BlogPost, Testimonial, Service, ContactMessage
from apps.parameters.widgets import Base64ImageField
import json


class CategoryForm(forms.ModelForm):
    """Form for Category model with color picker and icon selection"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Web Development'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of this category...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'title': 'Choose category color'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., bi-code-slash'
            })
        }


class TechnologyForm(forms.ModelForm):
    """Form for Technology model with proficiency validation"""
    
    class Meta:
        model = Technology
        fields = ['name', 'description', 'icon', 'website_url', 'proficiency', 'years_experience']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of this technology...'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., bi-code'
            }),
            'website_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.python.org'
            }),
            'proficiency': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 5
            }),
            'years_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 50,
                'step': 0.5
            })
        }
    
    def clean_proficiency(self):
        proficiency = self.cleaned_data.get('proficiency')
        if proficiency is not None and (proficiency < 0 or proficiency > 100):
            raise forms.ValidationError("Proficiency must be between 0 and 100")
        return proficiency


class ProjectForm(forms.ModelForm):
    """Form for Project model with image handling and technology selection"""
    
    # Custom image field
    featured_image_file = Base64ImageField(
        label="Featured Image",
        help_text="Upload project featured image (recommended: 1200x800px)",
        required=False
    )
    
    # Gallery images field
    gallery_images_json = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial='[]'
    )
    
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'description', 'detailed_description', 'project_type', 'status',
            'category', 'technologies', 'live_url', 'github_url', 'documentation_url',
            'start_date', 'end_date', 'client', 'team_size', 'key_features', 'challenges', 
            'solutions', 'results', 'meta_title', 'meta_description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL slug (auto-generated)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief project description for listings...'
            }),
            'detailed_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Detailed project description with features, challenges, and solutions...'
            }),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'technologies': forms.CheckboxSelectMultiple(),
            'live_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repo'
            }),
            'documentation_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://docs.example.com'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'client': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client or company name'
            }),
            'team_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100
            }),
            'key_features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'JSON array of key features, e.g., ["Feature 1", "Feature 2"]'
            }),
            'challenges': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the main challenges faced during this project...'
            }),
            'solutions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain how the challenges were solved...'
            }),
            'results': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the outcomes, impact, and results of this project...'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (max 60 characters)',
                'maxlength': 60
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (max 160 characters)',
                'maxlength': 160
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial image data if editing
        if self.instance.pk and self.instance.featured_image:
            self.fields['featured_image_file'].initial = self.instance.featured_image
        
        # Set initial gallery images
        if self.instance.pk and self.instance.gallery_images:
            self.fields['gallery_images_json'].initial = self.instance.gallery_images
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle featured image
        featured_image = self.cleaned_data.get('featured_image_file')
        if featured_image:
            instance.featured_image = featured_image
        
        # Handle gallery images
        gallery_json = self.cleaned_data.get('gallery_images_json')
        if gallery_json:
            instance.gallery_images = gallery_json
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance


class BlogPostForm(forms.ModelForm):
    """Form for BlogPost model with content editing and image handling"""
    
    # Custom image field
    featured_image_file = Base64ImageField(
        label="Featured Image",
        help_text="Upload blog post featured image (recommended: 800x600px)",
        required=False
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'excerpt', 'content', 'category', 'tags', 'status',
            'meta_title', 'meta_description', 'published_at', 'reading_time'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Blog post title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief excerpt for listings (max 300 characters)...',
                'maxlength': 300
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Blog post content in Markdown or HTML...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'tag1, tag2, tag3'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (max 60 characters)',
                'maxlength': 60
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (max 160 characters)',
                'maxlength': 160
            }),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'reading_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 120,
                'placeholder': 'e.g., 5'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial image data if editing
        if self.instance.pk and self.instance.featured_image:
            self.fields['featured_image_file'].initial = self.instance.featured_image
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle featured image
        featured_image = self.cleaned_data.get('featured_image_file')
        if featured_image:
            instance.featured_image = featured_image
        
        if commit:
            instance.save()
        
        return instance


class TestimonialForm(forms.ModelForm):
    """Form for Testimonial model with client photo handling"""
    
    # Custom image field for client photo
    client_photo_file = Base64ImageField(
        label="Client Photo",
        help_text="Upload client photo (will be resized to 200x200px)",
        required=False
    )
    
    class Meta:
        model = Testimonial
        fields = [
            'client_name', 'client_position', 'client_company', 'client_email',
            'content', 'rating', 'project', 'is_featured', 'is_approved'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client full name'
            }),
            'client_position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job title or position'
            }),
            'client_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'client@example.com'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Client testimonial content...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5
            }),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial image data if editing
        if self.instance.pk and self.instance.client_photo:
            self.fields['client_photo_file'].initial = self.instance.client_photo
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5")
        return rating
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Handle client photo
        client_photo = self.cleaned_data.get('client_photo_file')
        if client_photo:
            instance.client_photo = client_photo
        
        if commit:
            instance.save()
        
        return instance


class ServiceForm(forms.ModelForm):
    """Form for Service model with pricing and technology selection"""
    
    class Meta:
        model = Service
        fields = [
            'name', 'slug', 'short_description', 'description', 'icon', 'technologies',
            'delivery_time', 'features', 'process_steps',
            'starting_price', 'price_unit', 'is_active', 'is_featured', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL slug (auto-generated)'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description (max 200 characters)',
                'maxlength': 200
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed service description...'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., bi-code-slash'
            }),
            'technologies': forms.CheckboxSelectMultiple(),
            'delivery_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2-4 weeks'
            }),
            'features': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '["Feature 1", "Feature 2", "Feature 3"]'
            }),
            'process_steps': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '["Step 1", "Step 2", "Step 3"]'
            }),
            'starting_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 0.01
            }),
            'price_unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., per project, per hour'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            })
        }


class ContactMessageStatusForm(forms.ModelForm):
    """Form for updating contact message status"""
    
    class Meta:
        model = ContactMessage
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }


# Bulk action forms
class BulkDeleteForm(forms.Form):
    """Form for bulk delete operations"""
    selected_items = forms.CharField(widget=forms.HiddenInput())
    
    def clean_selected_items(self):
        data = self.cleaned_data['selected_items']
        try:
            item_ids = [int(x) for x in data.split(',') if x.strip()]
            if not item_ids:
                raise forms.ValidationError("No items selected")
            return item_ids
        except ValueError:
            raise forms.ValidationError("Invalid item selection")


class BulkStatusForm(forms.Form):
    """Form for bulk status updates"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('featured', 'Featured'),
        ('archived', 'Archived'),
    ]
    
    selected_items = forms.CharField(widget=forms.HiddenInput())
    new_status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def clean_selected_items(self):
        data = self.cleaned_data['selected_items']
        try:
            item_ids = [int(x) for x in data.split(',') if x.strip()]
            if not item_ids:
                raise forms.ValidationError("No items selected")
            return item_ids
        except ValueError:
            raise forms.ValidationError("Invalid item selection")
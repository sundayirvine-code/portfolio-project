from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Technology, Project, BlogPost, 
    Testimonial, Service, ContactMessage
)
from .widgets import Base64ImageWidget, MultipleBase64ImageWidget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for categories"""
    
    list_display = ('name', 'slug', 'color_preview', 'icon', 'color', 'created_at')
    list_editable = ('color',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description', 'icon', 'color')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Admin interface for technologies"""
    
    list_display = ('name', 'proficiency', 'years_experience', 'icon', 'created_at')
    list_editable = ('proficiency', 'years_experience')
    list_filter = ('proficiency', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Technology Information', {
            'fields': ('name', 'slug', 'description', 'icon', 'website_url')
        }),
        ('Experience Level', {
            'fields': ('proficiency', 'years_experience')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for projects"""
    
    list_display = ('title', 'project_type', 'status', 'category', 'start_date', 'is_published')
    list_editable = ('status',)
    list_filter = ('status', 'project_type', 'category', 'technologies')
    search_fields = ('title', 'description', 'detailed_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'slug', 'description', 'detailed_description')
        }),
        ('Project Details', {
            'fields': ('project_type', 'status', 'category', 'technologies')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery_images')
        }),
        ('Links', {
            'fields': ('live_url', 'github_url', 'documentation_url')
        }),
        ('Timeline & Team', {
            'fields': ('start_date', 'end_date', 'client', 'team_size')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['featured_image'].widget = Base64ImageWidget()
        form.base_fields['gallery_images'].widget = MultipleBase64ImageWidget()
        return form
    
    def is_published(self, obj):
        return obj.is_published
    is_published.boolean = True
    is_published.short_description = 'Published'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface for blog posts"""
    
    list_display = ('title', 'author', 'category', 'status', 'published_at', 'views_count')
    list_editable = ('status',)
    list_filter = ('status', 'category', 'author', 'published_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags', 'status')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Publishing', {
            'fields': ('published_at',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['featured_image'].widget = Base64ImageWidget()
        return form
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for testimonials"""
    
    list_display = ('client_name', 'client_company', 'rating', 'project', 'is_featured', 'is_approved')
    list_editable = ('is_featured', 'is_approved', 'rating')
    list_filter = ('rating', 'is_featured', 'is_approved', 'project')
    search_fields = ('client_name', 'client_company', 'content')
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_position', 'client_company', 'client_email', 'client_photo')
        }),
        ('Testimonial', {
            'fields': ('content', 'rating', 'project')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['client_photo'].widget = Base64ImageWidget()
        return form


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin interface for services"""
    
    list_display = ('name', 'starting_price', 'price_unit', 'is_active', 'is_featured', 'order')
    list_editable = ('is_active', 'is_featured', 'order', 'starting_price')
    list_filter = ('is_active', 'is_featured', 'technologies')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('technologies',)
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'slug', 'short_description', 'description', 'icon')
        }),
        ('Technical Details', {
            'fields': ('technologies',)
        }),
        ('Pricing', {
            'fields': ('starting_price', 'price_unit')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for contact messages"""
    
    list_display = ('name', 'email', 'subject', 'service_interest', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'service_interest', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'service_interest')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual creation of contact messages"""
        return False

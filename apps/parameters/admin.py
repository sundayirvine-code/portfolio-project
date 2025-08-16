from django.contrib import admin
from .models import SiteParameter, NavigationMenu, ColorPalette, FontPalette, ProfessionalJourney, FAQ, QuickAnswer


@admin.register(SiteParameter)
class SiteParameterAdmin(admin.ModelAdmin):
    """Admin interface for site parameters"""
    
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'site_url')
        }),
        ('Owner Information', {
            'fields': ('owner_name', 'owner_title', 'profile_image_base64')
        }),
        ('Theme Settings', {
            'fields': ('active_theme', 'default_mode')
        }),
        ('Typography Settings', {
            'fields': ('active_font_palette', 'base_font_size', 'heading_font_scale', 'small_font_scale')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Dynamic About Content', {
            'fields': ('about_me_text', 'my_story_text', 'bio'),
            'classes': ('collapse',)
        }),
        ('Values & Interests (JSON)', {
            'fields': ('values_interests',),
            'classes': ('collapse',),
            'description': 'Store as JSON format. See documentation for structure.'
        }),
        ('Fun Facts (JSON)', {
            'fields': ('fun_facts',),
            'classes': ('collapse',),
            'description': 'Store as JSON format. See documentation for structure.'
        }),
        ('Availability & Contact', {
            'fields': ('availability_status', 'availability_message', 'response_time'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('google_analytics_id',),
            'classes': ('collapse',)
        }),
        ('Social Media Links', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Feature Flags', {
            'fields': ('enable_blog', 'enable_testimonials', 'enable_contact_form', 'enable_animations')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    # Add list display for better overview
    list_display = ('site_name', 'owner_name', 'active_theme', 'default_mode', 'updated_at')
    
    # Add search functionality
    search_fields = ('site_name', 'owner_name', 'site_description')
    
    # Custom form help
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Add help text for JSON fields
        if 'values_interests' in form.base_fields:
            form.base_fields['values_interests'].help_text = (
                'JSON format: {"values": [{"name": "Innovation", "description": "...", "icon": "lightbulb", "color": "warning"}], '
                '"interests": [{"name": "Web Development", "description": "..."}]}'
            )
        
        if 'fun_facts' in form.base_fields:
            form.base_fields['fun_facts'].help_text = (
                'JSON format: [{"label": "Cups of Coffee", "value": 2847, "color": "primary"}, '
                '{"label": "Projects Completed", "value": 87, "color": "success"}]'
            )
        
        return form
    
    def has_add_permission(self, request):
        """Only allow one site parameter instance"""
        return not SiteParameter.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of site parameters"""
        return False


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    """Admin interface for navigation menu"""
    
    list_display = ('title', 'url', 'order', 'is_active', 'is_external', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'is_external', 'created_at')
    search_fields = ('title', 'url')
    ordering = ('order', 'title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Menu Item', {
            'fields': ('title', 'url', 'icon')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'is_external')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ColorPalette)
class ColorPaletteAdmin(admin.ModelAdmin):
    """Admin interface for color palettes"""
    
    list_display = ('name', 'slug', 'is_active', 'is_default', 'created_at')
    list_editable = ('is_active', 'is_default')
    list_filter = ('is_active', 'is_default', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Palette Information', {
            'fields': ('name', 'slug')
        }),
        ('Light Mode Colors', {
            'fields': ('light_primary', 'light_secondary', 'light_accent', 'light_background', 'light_text')
        }),
        ('Dark Mode Colors', {
            'fields': ('dark_primary', 'dark_secondary', 'dark_accent', 'dark_background', 'dark_text')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_default')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/color_picker.css',)
        }
        js = ('admin/js/color_picker.js',)


@admin.register(FontPalette)
class FontPaletteAdmin(admin.ModelAdmin):
    """Admin interface for font palettes"""
    
    list_display = ('name', 'slug', 'is_active', 'is_default', 'created_at')
    list_editable = ('is_active', 'is_default')
    list_filter = ('is_active', 'is_default', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Palette Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Font Configuration', {
            'fields': ('heading_font', 'body_font', 'accent_font')
        }),
        ('Font Weights & Sizes', {
            'fields': ('heading_weight', 'body_weight', 'base_font_size')
        }),
        ('Google Fonts', {
            'fields': ('google_fonts_url',),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active', 'is_default')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProfessionalJourney)
class ProfessionalJourneyAdmin(admin.ModelAdmin):
    """Admin interface for professional journey entries"""
    
    list_display = ('title', 'company', 'entry_type', 'start_date', 'is_current', 'is_featured', 'is_active', 'order')
    list_editable = ('is_featured', 'is_active', 'order')
    list_filter = ('entry_type', 'is_current', 'is_active', 'start_date')
    search_fields = ('title', 'company', 'location', 'description')
    date_hierarchy = 'start_date'
    ordering = ('-start_date', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'entry_type', 'location')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Content', {
            'fields': ('description', 'achievements', 'technologies')
        }),
        ('Settings', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', '-start_date')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin interface for FAQ entries"""
    
    list_display = ('question', 'category', 'is_featured', 'is_active', 'order', 'created_at')
    list_editable = ('is_featured', 'is_active', 'order')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('question', 'answer')
    ordering = ('order', 'category')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('FAQ Content', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Settings', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(QuickAnswer)
class QuickAnswerAdmin(admin.ModelAdmin):
    """Admin interface for quick answers"""
    
    list_display = ('question', 'is_active', 'order', 'created_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('question', 'answer')
    ordering = ('order',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Quick Answer', {
            'fields': ('question', 'answer', 'icon')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

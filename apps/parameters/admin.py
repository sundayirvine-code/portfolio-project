from django.contrib import admin
from .models import SiteParameter, NavigationMenu, ColorPalette, FontPalette, ProfessionalJourney, FAQ, QuickAnswer


@admin.register(SiteParameter)
class SiteParameterAdmin(admin.ModelAdmin):
    """Admin interface for site parameters"""
    
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'site_url')
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
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id',)
        }),
        ('Social Media', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url', 'instagram_url')
        }),
        ('Feature Flags', {
            'fields': ('enable_blog', 'enable_testimonials', 'enable_contact_form', 'enable_animations')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        """Only allow one site parameter instance"""
        return not SiteParameter.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of site parameters"""
        return False


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    """Admin interface for navigation menu"""
    
    list_display = ('title', 'url', 'order', 'is_active', 'is_external')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'is_external')
    search_fields = ('title', 'url')
    ordering = ('order', 'title')
    
    fieldsets = (
        ('Menu Item', {
            'fields': ('title', 'url', 'icon')
        }),
        ('Settings', {
            'fields': ('order', 'is_active', 'is_external')
        }),
    )


@admin.register(ColorPalette)
class ColorPaletteAdmin(admin.ModelAdmin):
    """Admin interface for color palettes"""
    
    list_display = ('name', 'slug', 'is_active', 'is_default')
    list_editable = ('is_active', 'is_default')
    list_filter = ('is_active', 'is_default')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
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
    )
    
    class Media:
        css = {
            'all': ('admin/css/color_picker.css',)
        }
        js = ('admin/js/color_picker.js',)


@admin.register(FontPalette)
class FontPaletteAdmin(admin.ModelAdmin):
    """Admin interface for font palettes"""
    
    list_display = ('name', 'slug', 'is_default', 'created_at')
    list_editable = ('is_default',)
    list_filter = ('is_default', 'created_at')
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
        ('Google Fonts', {
            'fields': ('google_fonts_url',)
        }),
        ('Settings', {
            'fields': ('is_default',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProfessionalJourney)
class ProfessionalJourneyAdmin(admin.ModelAdmin):
    """Admin interface for professional journey entries"""
    
    list_display = ('title', 'company', 'entry_type', 'start_date', 'is_current', 'is_active', 'order')
    list_editable = ('is_active', 'order')
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
            'fields': ('order', 'is_active')
        }),
    )
    
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
    
    fieldsets = (
        ('FAQ Content', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Settings', {
            'fields': ('order', 'is_featured', 'is_active')
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
    
    fieldsets = (
        ('Quick Answer', {
            'fields': ('question', 'answer')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

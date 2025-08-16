from django.contrib import admin
from .models import SiteParameter, NavigationMenu, ColorPalette


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

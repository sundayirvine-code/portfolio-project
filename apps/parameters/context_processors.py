from .models import SiteParameter, NavigationMenu, ColorPalette


def site_parameters(request):
    """
    Context processor to make site parameters available in all templates
    """
    try:
        settings = SiteParameter.get_settings()
        navigation_items = NavigationMenu.objects.filter(is_active=True)
        
        # Get active color palette or default
        try:
            active_palette = ColorPalette.objects.get(slug=settings.active_theme)
        except ColorPalette.DoesNotExist:
            active_palette = ColorPalette.objects.filter(is_default=True).first()
            if not active_palette:
                active_palette = ColorPalette.objects.first()
        
        return {
            'site_settings': settings,
            'navigation_items': navigation_items,
            'active_palette': active_palette,
        }
    except Exception:
        # Return default values if models haven't been migrated yet
        return {
            'site_settings': None,
            'navigation_items': [],
            'active_palette': None,
        }
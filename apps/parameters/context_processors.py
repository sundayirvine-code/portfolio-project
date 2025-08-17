from .models import SiteParameter, NavigationMenu, ColorPalette, ProfessionalJourney
import json


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
        
        # Get professional journey entries for work experience
        professional_journey = ProfessionalJourney.objects.filter(
            is_active=True,
            entry_type='work'
        ).order_by('-start_date', 'order')
        
        # Get education history
        education_history = ProfessionalJourney.objects.filter(
            is_active=True,
            entry_type='education'
        ).order_by('-start_date', 'order')
        
        # Parse JSON fields for fun facts and values
        fun_facts_list = []
        values_list = []
        
        if settings and settings.fun_facts:
            try:
                if isinstance(settings.fun_facts, str):
                    fun_facts_list = json.loads(settings.fun_facts)
                elif isinstance(settings.fun_facts, list):
                    fun_facts_list = settings.fun_facts
                elif isinstance(settings.fun_facts, dict):
                    fun_facts_list = [settings.fun_facts]
            except (json.JSONDecodeError, TypeError):
                fun_facts_list = []
        
        if settings and settings.values_interests:
            try:
                if isinstance(settings.values_interests, str):
                    values_data = json.loads(settings.values_interests)
                elif isinstance(settings.values_interests, dict):
                    values_data = settings.values_interests
                else:
                    values_data = {}
                
                # Extract values from the JSON structure
                values_list = values_data.get('values', [])
            except (json.JSONDecodeError, TypeError):
                values_list = []
        
        return {
            'site_settings': settings,
            'navigation_items': navigation_items,
            'active_palette': active_palette,
            'professional_journey': professional_journey,
            'education_history': education_history,
            'fun_facts_list': fun_facts_list,
            'values_list': values_list,
        }
    except Exception:
        # Return default values if models haven't been migrated yet
        return {
            'site_settings': None,
            'navigation_items': [],
            'active_palette': None,
            'professional_journey': [],
            'education_history': [],
            'fun_facts_list': [],
            'values_list': [],
        }
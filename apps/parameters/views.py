from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from .models import SiteParameter, NavigationMenu, ColorPalette, FontPalette, ProfessionalJourney, FAQ, QuickAnswer
from .forms import SiteParameterForm, NavigationMenuForm, ColorPaletteForm, ExtendedSiteParameterForm, FontPaletteForm, ProfessionalJourneyForm, FAQForm, QuickAnswerForm
from .json_forms import FunFactsManagerForm, ValuesManagerForm
import json


@staff_member_required
def parameter_dashboard(request):
    """Main parameter management dashboard"""
    site_settings = SiteParameter.get_settings()
    navigation_items = NavigationMenu.objects.all()[:5]  # Recent 5
    color_palettes = ColorPalette.objects.all()[:4]  # Recent 4
    
    context = {
        'site_settings': site_settings,
        'navigation_items': navigation_items,
        'color_palettes': color_palettes,
        'nav_count': NavigationMenu.objects.count(),
        'palette_count': ColorPalette.objects.count(),
    }
    
    return render(request, 'parameters/dashboard.html', context)


@staff_member_required
def site_settings_view(request):
    """Site settings management view"""
    site_settings = SiteParameter.get_settings()
    
    if request.method == 'POST':
        form = SiteParameterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully!')
            return redirect('parameters:site_settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SiteParameterForm(instance=site_settings)
    
    context = {
        'form': form,
        'site_settings': site_settings,
    }
    
    return render(request, 'parameters/site_settings.html', context)


@staff_member_required
def navigation_list_view(request):
    """Navigation menu management list view"""
    navigation_items = NavigationMenu.objects.all().order_by('order', 'title')
    
    context = {
        'navigation_items': navigation_items,
    }
    
    return render(request, 'parameters/navigation_list.html', context)


@staff_member_required
def navigation_create_view(request):
    """Create new navigation menu item"""
    if request.method == 'POST':
        form = NavigationMenuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Navigation item created successfully!')
            return redirect('parameters:navigation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NavigationMenuForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'parameters/navigation_form.html', context)


@staff_member_required
def navigation_edit_view(request, pk):
    """Edit navigation menu item"""
    navigation_item = get_object_or_404(NavigationMenu, pk=pk)
    
    if request.method == 'POST':
        form = NavigationMenuForm(request.POST, instance=navigation_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Navigation item updated successfully!')
            return redirect('parameters:navigation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NavigationMenuForm(instance=navigation_item)
    
    context = {
        'form': form,
        'navigation_item': navigation_item,
        'action': 'Edit',
    }
    
    return render(request, 'parameters/navigation_form.html', context)


@staff_member_required
@require_POST
def navigation_delete_view(request, pk):
    """Delete navigation menu item"""
    navigation_item = get_object_or_404(NavigationMenu, pk=pk)
    navigation_item.delete()
    messages.success(request, f'Navigation item "{navigation_item.title}" deleted successfully!')
    return redirect('parameters:navigation_list')


@staff_member_required
@require_POST
def navigation_toggle_active(request, pk):
    """Toggle navigation item active status"""
    navigation_item = get_object_or_404(NavigationMenu, pk=pk)
    navigation_item.is_active = not navigation_item.is_active
    navigation_item.save()
    
    status = "activated" if navigation_item.is_active else "deactivated"
    messages.success(request, f'Navigation item "{navigation_item.title}" {status}!')
    
    return JsonResponse({'success': True, 'is_active': navigation_item.is_active})


@staff_member_required
def color_palette_list_view(request):
    """Color palette management list view"""
    color_palettes = ColorPalette.objects.all().order_by('name')
    
    context = {
        'color_palettes': color_palettes,
    }
    
    return render(request, 'parameters/color_palette_list.html', context)


@staff_member_required
def color_palette_create_view(request):
    """Create new color palette"""
    if request.method == 'POST':
        form = ColorPaletteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Color palette created successfully!')
                return redirect('parameters:color_palette_list')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ColorPaletteForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'parameters/color_palette_form.html', context)


@staff_member_required
def color_palette_edit_view(request, pk):
    """Edit color palette"""
    color_palette = get_object_or_404(ColorPalette, pk=pk)
    
    if request.method == 'POST':
        form = ColorPaletteForm(request.POST, instance=color_palette)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Color palette updated successfully!')
                return redirect('parameters:color_palette_list')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ColorPaletteForm(instance=color_palette)
    
    context = {
        'form': form,
        'color_palette': color_palette,
        'action': 'Edit',
    }
    
    return render(request, 'parameters/color_palette_form.html', context)


@staff_member_required
@require_POST
def color_palette_delete_view(request, pk):
    """Delete color palette"""
    color_palette = get_object_or_404(ColorPalette, pk=pk)
    
    if color_palette.is_default:
        messages.error(request, 'Cannot delete the default color palette!')
        return redirect('parameters:color_palette_list')
    
    color_palette.delete()
    messages.success(request, f'Color palette "{color_palette.name}" deleted successfully!')
    return redirect('parameters:color_palette_list')


@staff_member_required
@require_POST
def color_palette_set_default(request, pk):
    """Set color palette as default"""
    color_palette = get_object_or_404(ColorPalette, pk=pk)
    
    # Remove default from all other palettes
    ColorPalette.objects.update(is_default=False)
    
    # Set this palette as default
    color_palette.is_default = True
    color_palette.save()
    
    messages.success(request, f'Color palette "{color_palette.name}" set as default!')
    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def apply_color_palette(request, pk):
    """Apply color palette to site settings"""
    color_palette = get_object_or_404(ColorPalette, pk=pk)
    site_settings = SiteParameter.get_settings()
    
    # Update active theme in site settings
    site_settings.active_theme = color_palette.slug
    site_settings.save()
    
    messages.success(request, f'Color palette "{color_palette.name}" applied to site!')
    return JsonResponse({'success': True})


@staff_member_required
def preview_color_palette(request, pk):
    """Preview color palette"""
    color_palette = get_object_or_404(ColorPalette, pk=pk)
    
    palette_data = {
        'name': color_palette.name,
        'light_colors': {
            'primary': color_palette.light_primary,
            'secondary': color_palette.light_secondary,
            'accent': color_palette.light_accent,
            'background': color_palette.light_background,
            'text': color_palette.light_text,
        },
        'dark_colors': {
            'primary': color_palette.dark_primary,
            'secondary': color_palette.dark_secondary,
            'accent': color_palette.dark_accent,
            'background': color_palette.dark_background,
            'text': color_palette.dark_text,
        }
    }
    
    return JsonResponse(palette_data)


# ===============================================================
# COMPREHENSIVE ADMIN CRUD VIEWS
# ===============================================================

@staff_member_required
def comprehensive_settings_view(request):
    """Comprehensive site settings management view"""
    site_settings = SiteParameter.get_settings()
    
    if request.method == 'POST':
        form = ExtendedSiteParameterForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully!')
            return redirect('parameters:comprehensive_settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExtendedSiteParameterForm(instance=site_settings)
    
    context = {
        'form': form,
        'site_settings': site_settings,
        'title': 'Site Settings',
    }
    
    return render(request, 'parameters/admin/comprehensive_settings.html', context)


@staff_member_required
def fun_facts_management(request):
    """Manage fun facts with user-friendly interface"""
    site_settings = SiteParameter.get_settings()
    
    # Parse existing fun facts
    try:
        if site_settings.fun_facts:
            if isinstance(site_settings.fun_facts, str):
                fun_facts_data = json.loads(site_settings.fun_facts)
            elif isinstance(site_settings.fun_facts, list):
                fun_facts_data = site_settings.fun_facts
            else:
                fun_facts_data = []
        else:
            fun_facts_data = []
    except (json.JSONDecodeError, TypeError):
        fun_facts_data = []
    
    if request.method == 'POST':
        form = FunFactsManagerForm(request.POST, initial_data=fun_facts_data)
        if form.is_valid():
            facts_data = form.get_facts_data()
            site_settings.fun_facts = facts_data
            site_settings.save()
            messages.success(request, 'Fun facts updated successfully!')
            return redirect('parameters:fun_facts_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FunFactsManagerForm(initial_data=fun_facts_data)
    
    context = {
        'form': form,
        'fun_facts_data': fun_facts_data,
        'title': 'Fun Facts Management',
    }
    
    return render(request, 'parameters/admin/fun_facts_management.html', context)


@staff_member_required
def values_interests_management(request):
    """Manage values and interests with user-friendly interface"""
    site_settings = SiteParameter.get_settings()
    
    # Parse existing values and interests
    try:
        if site_settings.values_interests:
            if isinstance(site_settings.values_interests, str):
                values_data = json.loads(site_settings.values_interests)
            else:
                values_data = site_settings.values_interests
        else:
            values_data = {}
    except (json.JSONDecodeError, TypeError):
        values_data = {}
    
    if request.method == 'POST':
        form = ValuesManagerForm(request.POST, initial_data=values_data)
        if form.is_valid():
            new_values_data = form.get_values_interests_data()
            site_settings.values_interests = new_values_data
            site_settings.save()
            messages.success(request, 'Values and interests updated successfully!')
            return redirect('parameters:values_interests_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ValuesManagerForm(initial_data=values_data)
    
    context = {
        'form': form,
        'values_data': values_data,
        'title': 'Values & Interests Management',
    }
    
    return render(request, 'parameters/admin/values_interests_management.html', context)


# ===============================================================
# FONT PALETTE CRUD VIEWS
# ===============================================================

@staff_member_required
def font_palette_list_view(request):
    """Font palette management list view"""
    font_palettes = FontPalette.objects.all().order_by('name')
    
    # Add pagination
    paginator = Paginator(font_palettes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'Font Palettes',
    }
    
    return render(request, 'parameters/admin/font_palette_list.html', context)


@staff_member_required
def font_palette_create_view(request):
    """Create new font palette"""
    if request.method == 'POST':
        form = FontPaletteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Font palette created successfully!')
            return redirect('parameters:font_palette_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FontPaletteForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Font Palette',
    }
    
    return render(request, 'parameters/admin/font_palette_form.html', context)


@staff_member_required
def font_palette_edit_view(request, pk):
    """Edit font palette"""
    font_palette = get_object_or_404(FontPalette, pk=pk)
    
    if request.method == 'POST':
        form = FontPaletteForm(request.POST, instance=font_palette)
        if form.is_valid():
            form.save()
            messages.success(request, 'Font palette updated successfully!')
            return redirect('parameters:font_palette_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FontPaletteForm(instance=font_palette)
    
    context = {
        'form': form,
        'font_palette': font_palette,
        'action': 'Edit',
        'title': f'Edit Font Palette: {font_palette.name}',
    }
    
    return render(request, 'parameters/admin/font_palette_form.html', context)


@staff_member_required
@require_POST
def font_palette_delete_view(request, pk):
    """Delete font palette"""
    font_palette = get_object_or_404(FontPalette, pk=pk)
    
    if font_palette.is_default:
        messages.error(request, 'Cannot delete the default font palette!')
        return redirect('parameters:font_palette_list')
    
    font_palette.delete()
    messages.success(request, f'Font palette "{font_palette.name}" deleted successfully!')
    return redirect('parameters:font_palette_list')


# ===============================================================
# PROFESSIONAL JOURNEY CRUD VIEWS
# ===============================================================

@staff_member_required
def professional_journey_list_view(request):
    """Professional journey management list view"""
    # Filter by entry type if specified
    entry_type = request.GET.get('type', '')
    if entry_type:
        entries = ProfessionalJourney.objects.filter(entry_type=entry_type).order_by('-start_date', 'order')
    else:
        entries = ProfessionalJourney.objects.all().order_by('-start_date', 'order')
    
    # Add pagination
    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_type': entry_type,
        'entry_types': ProfessionalJourney.ENTRY_TYPE_CHOICES,
        'title': 'Professional Journey',
    }
    
    return render(request, 'parameters/admin/professional_journey_list.html', context)


@staff_member_required
def professional_journey_create_view(request):
    """Create new professional journey entry"""
    if request.method == 'POST':
        form = ProfessionalJourneyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professional journey entry created successfully!')
            return redirect('parameters:professional_journey_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfessionalJourneyForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Add Professional Journey Entry',
    }
    
    return render(request, 'parameters/admin/professional_journey_form.html', context)


@staff_member_required
def professional_journey_edit_view(request, pk):
    """Edit professional journey entry"""
    entry = get_object_or_404(ProfessionalJourney, pk=pk)
    
    if request.method == 'POST':
        form = ProfessionalJourneyForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professional journey entry updated successfully!')
            return redirect('parameters:professional_journey_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfessionalJourneyForm(instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'action': 'Edit',
        'title': f'Edit Entry: {entry.title}',
    }
    
    return render(request, 'parameters/admin/professional_journey_form.html', context)


@staff_member_required
@require_POST
def professional_journey_delete_view(request, pk):
    """Delete professional journey entry"""
    entry = get_object_or_404(ProfessionalJourney, pk=pk)
    entry.delete()
    messages.success(request, f'Professional journey entry "{entry.title}" deleted successfully!')
    return redirect('parameters:professional_journey_list')


# ===============================================================
# FAQ CRUD VIEWS
# ===============================================================

@staff_member_required
def faq_list_view(request):
    """FAQ management list view"""
    # Filter by category if specified
    category = request.GET.get('category', '')
    if category:
        faqs = FAQ.objects.filter(category=category).order_by('order', 'category')
    else:
        faqs = FAQ.objects.all().order_by('order', 'category')
    
    # Add pagination
    paginator = Paginator(faqs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_category': category,
        'categories': FAQ.CATEGORY_CHOICES,
        'title': 'FAQ Management',
    }
    
    return render(request, 'parameters/admin/faq_list.html', context)


@staff_member_required
def faq_create_view(request):
    """Create new FAQ entry"""
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ entry created successfully!')
            return redirect('parameters:faq_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FAQForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Add FAQ Entry',
    }
    
    return render(request, 'parameters/admin/faq_form.html', context)


@staff_member_required
def faq_edit_view(request, pk):
    """Edit FAQ entry"""
    faq = get_object_or_404(FAQ, pk=pk)
    
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ entry updated successfully!')
            return redirect('parameters:faq_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FAQForm(instance=faq)
    
    context = {
        'form': form,
        'faq': faq,
        'action': 'Edit',
        'title': f'Edit FAQ: {faq.question[:50]}...',
    }
    
    return render(request, 'parameters/admin/faq_form.html', context)


@staff_member_required
@require_POST
def faq_delete_view(request, pk):
    """Delete FAQ entry"""
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, f'FAQ entry deleted successfully!')
    return redirect('parameters:faq_list')


# ===============================================================
# QUICK ANSWER CRUD VIEWS  
# ===============================================================

@staff_member_required
def quick_answer_list_view(request):
    """Quick answer management list view"""
    quick_answers = QuickAnswer.objects.all().order_by('order')
    
    # Add pagination
    paginator = Paginator(quick_answers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'Quick Answers',
    }
    
    return render(request, 'parameters/admin/quick_answer_list.html', context)


@staff_member_required
def quick_answer_create_view(request):
    """Create new quick answer"""
    if request.method == 'POST':
        form = QuickAnswerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quick answer created successfully!')
            return redirect('parameters:quick_answer_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuickAnswerForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Add Quick Answer',
    }
    
    return render(request, 'parameters/admin/quick_answer_form.html', context)


@staff_member_required
def quick_answer_edit_view(request, pk):
    """Edit quick answer"""
    quick_answer = get_object_or_404(QuickAnswer, pk=pk)
    
    if request.method == 'POST':
        form = QuickAnswerForm(request.POST, instance=quick_answer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quick answer updated successfully!')
            return redirect('parameters:quick_answer_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuickAnswerForm(instance=quick_answer)
    
    context = {
        'form': form,
        'quick_answer': quick_answer,
        'action': 'Edit',
        'title': f'Edit Quick Answer: {quick_answer.question[:50]}...',
    }
    
    return render(request, 'parameters/admin/quick_answer_form.html', context)


@staff_member_required
@require_POST
def quick_answer_delete_view(request, pk):
    """Delete quick answer"""
    quick_answer = get_object_or_404(QuickAnswer, pk=pk)
    quick_answer.delete()
    messages.success(request, f'Quick answer deleted successfully!')
    return redirect('parameters:quick_answer_list')

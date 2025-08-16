from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from .models import SiteParameter, NavigationMenu, ColorPalette
from .forms import SiteParameterForm, NavigationMenuForm, ColorPaletteForm


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

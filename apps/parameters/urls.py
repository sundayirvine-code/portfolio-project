from django.urls import path
from . import views

app_name = 'parameters'

urlpatterns = [
    # Parameter Dashboard
    path('dashboard/', views.parameter_dashboard, name='dashboard'),
    
    # Site Settings
    path('site-settings/', views.site_settings_view, name='site_settings'),
    
    # Navigation Management
    path('navigation/', views.navigation_list_view, name='navigation_list'),
    path('navigation/create/', views.navigation_create_view, name='navigation_create'),
    path('navigation/<int:pk>/edit/', views.navigation_edit_view, name='navigation_edit'),
    path('navigation/<int:pk>/delete/', views.navigation_delete_view, name='navigation_delete'),
    path('navigation/<int:pk>/toggle-active/', views.navigation_toggle_active, name='navigation_toggle_active'),
    
    # Color Palette Management
    path('color-palettes/', views.color_palette_list_view, name='color_palette_list'),
    path('color-palettes/create/', views.color_palette_create_view, name='color_palette_create'),
    path('color-palettes/<int:pk>/edit/', views.color_palette_edit_view, name='color_palette_edit'),
    path('color-palettes/<int:pk>/delete/', views.color_palette_delete_view, name='color_palette_delete'),
    path('color-palettes/<int:pk>/set-default/', views.color_palette_set_default, name='color_palette_set_default'),
    path('color-palettes/<int:pk>/apply/', views.apply_color_palette, name='apply_color_palette'),
    path('color-palettes/<int:pk>/preview/', views.preview_color_palette, name='preview_color_palette'),
]
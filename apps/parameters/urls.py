from django.urls import path
from . import views

app_name = 'parameters'

urlpatterns = [
    # Parameter Dashboard
    path('dashboard/', views.parameter_dashboard, name='dashboard'),
    
    # Site Settings
    path('site-settings/', views.site_settings_view, name='site_settings'),
    path('comprehensive-settings/', views.comprehensive_settings_view, name='comprehensive_settings'),
    
    # JSON Field Management
    path('fun-facts/', views.fun_facts_management, name='fun_facts_management'),
    path('values-interests/', views.values_interests_management, name='values_interests_management'),
    path('skills-expertise/', views.skills_expertise_management, name='skills_expertise_management'),
    
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
    
    # Font Palette Management
    path('font-palettes/', views.font_palette_list_view, name='font_palette_list'),
    path('font-palettes/create/', views.font_palette_create_view, name='font_palette_create'),
    path('font-palettes/<int:pk>/edit/', views.font_palette_edit_view, name='font_palette_edit'),
    path('font-palettes/<int:pk>/delete/', views.font_palette_delete_view, name='font_palette_delete'),
    
    # Professional Journey Management
    path('professional-journey/', views.professional_journey_list_view, name='professional_journey_list'),
    path('professional-journey/create/', views.professional_journey_create_view, name='professional_journey_create'),
    path('professional-journey/<int:pk>/edit/', views.professional_journey_edit_view, name='professional_journey_edit'),
    path('professional-journey/<int:pk>/delete/', views.professional_journey_delete_view, name='professional_journey_delete'),
    
    # FAQ Management
    path('faq/', views.faq_list_view, name='faq_list'),
    path('faq/create/', views.faq_create_view, name='faq_create'),
    path('faq/<int:pk>/edit/', views.faq_edit_view, name='faq_edit'),
    path('faq/<int:pk>/delete/', views.faq_delete_view, name='faq_delete'),
    
    # Quick Answer Management
    path('quick-answers/', views.quick_answer_list_view, name='quick_answer_list'),
    path('quick-answers/create/', views.quick_answer_create_view, name='quick_answer_create'),
    path('quick-answers/<int:pk>/edit/', views.quick_answer_edit_view, name='quick_answer_edit'),
    path('quick-answers/<int:pk>/delete/', views.quick_answer_delete_view, name='quick_answer_delete'),
]
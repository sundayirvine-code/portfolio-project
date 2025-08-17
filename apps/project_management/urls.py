from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Main pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('search/', views.search_view, name='search'),
    
    # Projects
    path('projects/', views.projects_view, name='projects'),
    path('projects/<slug:slug>/', views.project_detail_view, name='project_detail'),
    
    # Blog
    path('blog/', views.blog_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    
    # Services
    path('services/', views.services_view, name='services'),
    
    # Testimonials
    path('testimonials/', views.testimonials_view, name='testimonials'),
    
    # CV Preview and Download
    path('cv-preview/', views.cv_preview_view, name='cv_preview'),
    path('download-cv/', views.download_cv_view, name='download_cv'),
    
    # AJAX endpoints
    path('ajax/contact/', views.ajax_contact_view, name='ajax_contact'),
    
    # API endpoints
    path('api/search/', views.api_search_view, name='api_search'),
]
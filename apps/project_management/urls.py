from django.urls import path
from . import views, admin_views

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
    
    # ===============================================================
    # ADMIN MANAGEMENT ROUTES
    # ===============================================================
    
    # Category Management
    path('manage/categories/', admin_views.category_list, name='category_list'),
    path('manage/categories/create/', admin_views.category_create, name='category_create'),
    path('manage/categories/<int:pk>/edit/', admin_views.category_edit, name='category_edit'),
    path('manage/categories/<int:pk>/delete/', admin_views.category_delete, name='category_delete'),
    
    # Technology Management
    path('manage/technologies/', admin_views.technology_list, name='technology_list'),
    path('manage/technologies/create/', admin_views.technology_create, name='technology_create'),
    path('manage/technologies/<int:pk>/edit/', admin_views.technology_edit, name='technology_edit'),
    path('manage/technologies/<int:pk>/delete/', admin_views.technology_delete, name='technology_delete'),
    
    # Project Management
    path('manage/projects/', admin_views.project_list_admin, name='project_list'),
    path('manage/projects/create/', admin_views.project_create_admin, name='project_create'),
    path('manage/projects/<int:pk>/edit/', admin_views.project_edit_admin, name='project_edit'),
    path('manage/projects/<int:pk>/delete/', admin_views.project_delete_admin, name='project_delete'),
    
    # Blog Post Management
    path('manage/blog/', admin_views.blogpost_list, name='blogpost_list'),
    path('manage/blog/create/', admin_views.blogpost_create, name='blogpost_create'),
    path('manage/blog/<int:pk>/edit/', admin_views.blogpost_edit, name='blogpost_edit'),
    path('manage/blog/<int:pk>/delete/', admin_views.blogpost_delete, name='blogpost_delete'),
    
    # Testimonial Management
    path('manage/testimonials/', admin_views.testimonial_list, name='testimonial_list'),
    path('manage/testimonials/create/', admin_views.testimonial_create, name='testimonial_create'),
    path('manage/testimonials/<int:pk>/edit/', admin_views.testimonial_edit, name='testimonial_edit'),
    path('manage/testimonials/<int:pk>/delete/', admin_views.testimonial_delete, name='testimonial_delete'),
    
    # Service Management
    path('manage/services/', admin_views.service_list_admin, name='service_list'),
    path('manage/services/create/', admin_views.service_create_admin, name='service_create'),
    path('manage/services/<int:pk>/edit/', admin_views.service_edit_admin, name='service_edit'),
    path('manage/services/<int:pk>/delete/', admin_views.service_delete_admin, name='service_delete'),
    
    # Contact Messages
    path('manage/contacts/', admin_views.contact_messages, name='contact_messages'),
    path('manage/contacts/<int:pk>/', admin_views.contact_message_detail, name='contact_message_detail'),
    path('manage/contacts/<int:pk>/delete/', admin_views.contact_message_delete, name='contact_message_delete'),
    
    # Bulk Operations
    path('manage/bulk/delete/', admin_views.bulk_delete, name='bulk_delete'),
    path('manage/bulk/status/', admin_views.bulk_status_update, name='bulk_status_update'),
]
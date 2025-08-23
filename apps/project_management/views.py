from textwrap import indent
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q, Avg
from .models import Project, BlogPost, Testimonial, Service, ContactMessage, Category, Technology
from apps.parameters.models import SiteParameter, ProfessionalJourney, FAQ, QuickAnswer
from .forms import ContactForm
from .services import CVGenerationService


def home_view(request):
    """Home page view with featured content and dynamic fallbacks"""
    # Featured projects - try featured first, fallback to published if none
    featured_projects = Project.objects.filter(
        status='featured'
    ).select_related('category').prefetch_related('technologies')[:4]
    
    if not featured_projects.exists():
        # Fallback to latest published projects
        featured_projects = Project.objects.filter(
            status='published'
        ).select_related('category').prefetch_related('technologies').order_by('-created_at')[:4]
    
    # Featured Blog Posts - try featured first, fallback to recent published
    recent_posts = BlogPost.objects.filter(
        status='featured'
    ).select_related('author', 'category')[:3]
    
    if not recent_posts.exists():
        # Fallback to latest published posts
        recent_posts = BlogPost.objects.filter(
            status='published'
        ).select_related('author', 'category').order_by('-published_at')[:3]
    
    # Featured testimonials with fallback
    featured_testimonials = Testimonial.objects.filter(
        is_featured=True, 
        is_approved=True
    ).select_related('project')[:3]
    
    if not featured_testimonials.exists():
        # Fallback to latest approved testimonials
        featured_testimonials = Testimonial.objects.filter(
            is_approved=True
        ).select_related('project').order_by('-created_at')[:3]
    
    # Featured services with fallback
    featured_services = Service.objects.filter(
        is_active=True, 
        is_featured=True
    ).prefetch_related('technologies')[:3]
    
    if not featured_services.exists():
        # Fallback to latest active services
        featured_services = Service.objects.filter(
            is_active=True
        ).prefetch_related('technologies').order_by('-created_at')[:3]
    
    # Get site settings for dynamic homepage content
    site_settings = SiteParameter.get_settings()
    
    context = {
        'featured_projects': featured_projects,
        'recent_posts': recent_posts,
        'featured_testimonials': featured_testimonials,
        'featured_services': featured_services,
        'site_settings': site_settings,
    }
    
    return render(request, 'pages/home.html', context)


def about_view(request):
    """About page view with dynamic content"""
    # Top technologies by proficiency
    top_technologies = Technology.objects.filter(
        proficiency__gte=70
    ).order_by('-proficiency', '-years_experience')[:10]
    
    # All technologies grouped by proficiency
    technologies = Technology.objects.all().order_by('-proficiency', 'name')
    
    # Professional journey (work experience, education, etc.)
    professional_journey = ProfessionalJourney.objects.filter(
        is_active=True
    ).order_by('-start_date')
    
    # Separate by type for different sections
    work_experience = professional_journey.filter(entry_type='work').order_by('-start_date', 'order')
    education_history = professional_journey.filter(entry_type='education').order_by('-start_date', 'order')
    certifications = professional_journey.filter(entry_type='certification').order_by('-start_date', 'order')
    achievements = professional_journey.filter(entry_type='achievement').order_by('-start_date', 'order')
    major_projects = professional_journey.filter(entry_type='project').order_by('-start_date', 'order')
    
    # Create a dictionary for easy template access with counts
    journey_data = {
        'work': {
            'entries': work_experience,
            'count': work_experience.count(),
            'label': 'Work Experience',
            'icon': 'briefcase'
        },
        'education': {
            'entries': education_history,
            'count': education_history.count(),
            'label': 'Education',
            'icon': 'mortarboard'
        },
        'certification': {
            'entries': certifications,
            'count': certifications.count(),
            'label': 'Certifications',
            'icon': 'award'
        },
        'achievement': {
            'entries': achievements,
            'count': achievements.count(),
            'label': 'Achievements',
            'icon': 'trophy'
        },
        'project': {
            'entries': major_projects,
            'count': major_projects.count(),
            'label': 'Major Projects',
            'icon': 'lightbulb'
        }
    }
    
    # Get site settings for dynamic content
    site_settings = SiteParameter.get_settings()
    import json
    # print(json.loads(site_settings, indent=2))
    
    # Parse JSON fields for dynamic content with fallbacks
    fun_facts_list = []
    values_list = []
    skills_list = []
    
    try:
        import json
        if hasattr(site_settings, 'fun_facts') and site_settings.fun_facts:
            fun_facts_list = json.loads(site_settings.fun_facts) if isinstance(site_settings.fun_facts, str) else site_settings.fun_facts
        
        if hasattr(site_settings, 'values_interests') and site_settings.values_interests:
            values_data = json.loads(site_settings.values_interests) if isinstance(site_settings.values_interests, str) else site_settings.values_interests
            
            # Handle both legacy dict format and new list format
            if isinstance(values_data, dict):
                # Legacy format: {'values': [...], 'interests': [...]}
                legacy_values = values_data.get('values', [])
                legacy_interests = values_data.get('interests', [])
                
                # Convert to new format
                values_list = []
                for value in legacy_values:
                    if isinstance(value, str):
                        values_list.append({
                            'name': value,
                            'description': '',
                            'icon': 'heart',
                            'color': 'primary'
                        })
                    elif isinstance(value, dict):
                        values_list.append(value)
                        
                for interest in legacy_interests:
                    if isinstance(interest, str):
                        values_list.append({
                            'name': interest,
                            'description': '',
                            'icon': 'star',
                            'color': 'info'
                        })
                    elif isinstance(interest, dict):
                        values_list.append(interest)
            elif isinstance(values_data, list):
                # New format: list of value objects
                values_list = values_data
            else:
                values_list = []
        
        if hasattr(site_settings, 'skills_expertise') and site_settings.skills_expertise:
            skills_data = json.loads(site_settings.skills_expertise) if isinstance(site_settings.skills_expertise, str) else site_settings.skills_expertise
            if isinstance(skills_data, list):
                skills_list = skills_data
            else:
                skills_list = []
    except (json.JSONDecodeError, AttributeError, TypeError):
        pass  # Use default fallbacks in template
    
    context = {
        'top_technologies': top_technologies,
        'technologies': technologies,
        'professional_journey': professional_journey,
        'journey_data': journey_data,
        # Keep old structure for backwards compatibility
        'work_experience': work_experience,
        'education_history': education_history,
        'certifications': certifications,
        'achievements': achievements,
        'major_projects': major_projects,
        'fun_facts_list': fun_facts_list,
        'values_list': values_list,
        'skills_list': skills_list,
        'site_settings': site_settings,
    }
    
    return render(request, 'pages/about.html', context)


def projects_view(request):
    """Projects portfolio view with filtering"""
    projects = Project.objects.filter(
        status__in=['published', 'featured']
    ).select_related('category').prefetch_related('technologies')
    
    # Filtering
    category_filter = request.GET.get('category')
    technology_filter = request.GET.get('technology')
    type_filter = request.GET.get('type')
    search_query = request.GET.get('search')
    
    if category_filter:
        projects = projects.filter(category__slug=category_filter)
    
    if technology_filter:
        projects = projects.filter(technologies__slug=technology_filter)
    
    if type_filter:
        projects = projects.filter(project_type=type_filter)
    
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(detailed_description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(projects, 9)  # 9 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options
    categories = Category.objects.all()
    technologies = Technology.objects.all()
    project_types = Project.TYPE_CHOICES
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'technologies': technologies,
        'project_types': project_types,
        'current_category': category_filter,
        'current_technology': technology_filter,
        'current_type': type_filter,
        'search_query': search_query,
    }
    
    return render(request, 'pages/projects.html', context)


def project_detail_view(request, slug):
    """Individual project detail view"""
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related('technologies', 'testimonials'),
        slug=slug,
        status__in=['published', 'featured']
    )
    
    # Related projects
    related_projects = Project.objects.filter(
        status__in=['published', 'featured']
    ).exclude(id=project.id)
    
    if project.category:
        related_projects = related_projects.filter(category=project.category)
    
    related_projects = related_projects[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'pages/project_detail.html', context)


def blog_view(request):
    """Blog listing view"""
    posts = BlogPost.objects.filter(
        status__in=['published', 'featured']
    ).select_related('author', 'category')
    
    # Filtering
    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    search_query = request.GET.get('search')
    
    if category_filter:
        posts = posts.filter(category__slug=category_filter)
    
    if tag_filter:
        posts = posts.filter(tags__icontains=tag_filter)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.all()
    
    # Get all tags
    all_tags = []
    for post in BlogPost.objects.filter(status__in=['published', 'featured']):
        all_tags.extend(post.tag_list)
    unique_tags = list(set(all_tags))
    
    # Recent posts
    recent_posts = BlogPost.objects.filter(
        status__in=['published', 'featured']
    ).order_by('-published_at')[:5]
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': unique_tags,
        'recent_posts': recent_posts,
        'current_category': category_filter,
        'current_tag': tag_filter,
        'search_query': search_query,
    }
    
    return render(request, 'pages/blog.html', context)


def blog_detail_view(request, slug):
    """Individual blog post detail view"""
    post = get_object_or_404(
        BlogPost.objects.select_related('author', 'category'),
        slug=slug,
        status__in=['published', 'featured']
    )
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Related posts
    related_posts = BlogPost.objects.filter(
        status__in=['published', 'featured']
    ).exclude(id=post.id)
    
    if post.category:
        related_posts = related_posts.filter(category=post.category)
    
    related_posts = related_posts[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'pages/blog_detail.html', context)


def services_view(request):
    """Services and skills view"""
    services = Service.objects.filter(is_active=True).prefetch_related('technologies')
    
    # Group technologies by proficiency level
    expert_technologies = Technology.objects.filter(proficiency__gte=90)
    advanced_technologies = Technology.objects.filter(proficiency__gte=70, proficiency__lt=90)
    intermediate_technologies = Technology.objects.filter(proficiency__gte=50, proficiency__lt=70)
    
    # Get FAQs for services page
    from apps.parameters.models import FAQ
    service_faqs = FAQ.objects.filter(
        is_active=True
    ).order_by('order', 'id')
    
    context = {
        'services': services,
        'expert_technologies': expert_technologies,
        'advanced_technologies': advanced_technologies,
        'intermediate_technologies': intermediate_technologies,
        'faqs': service_faqs,
    }
    
    return render(request, 'pages/services.html', context)


def testimonials_view(request):
    """Testimonials view"""
    testimonials = Testimonial.objects.filter(
        is_approved=True
    ).select_related('project').order_by('display_order', '-date_given', '-created_at')
    
    # Calculate statistics
    total_testimonials = testimonials.count()
    if total_testimonials > 0:
        average_rating = testimonials.aggregate(avg_rating=Avg('rating'))['avg_rating']
        average_rating = round(average_rating, 1) if average_rating else 5.0
    else:
        average_rating = 5.0
    
    # Get featured testimonials count
    featured_count = testimonials.filter(is_featured=True).count()
    
    # Pagination
    paginator = Paginator(testimonials, 6)  # 6 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'testimonials': page_obj,  # For compatibility with template
        'total_testimonials': total_testimonials,
        'average_rating': average_rating,
        'featured_count': featured_count,
        'projects_completed': Project.objects.filter(status__in=['published', 'featured']).count(),
        'repeat_clients': 85,  # This could be calculated based on client_email duplicates
    }
    
    return render(request, 'pages/testimonials.html', context)


def contact_view(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            
            # Add metadata
            contact_message.ip_address = request.META.get('REMOTE_ADDR')
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            contact_message.save()
            
            messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
            return render(request, 'pages/contact.html', {'form': ContactForm()})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    # Get site settings for availability information
    site_settings = SiteParameter.get_settings()
    
    # Services for dropdown
    services = Service.objects.filter(is_active=True)
    
    # Get Quick Answers first (priority over FAQs)
    quick_answers = QuickAnswer.objects.filter(is_active=True).order_by('order')[:5]
    
    # Get featured FAQs if no quick answers
    featured_faqs = FAQ.objects.filter(
        is_active=True, 
        is_featured=True, 
        category='contact'
    ).order_by('order')[:5]
    
    # If no contact-specific featured FAQs, get general featured FAQs
    if not featured_faqs and not quick_answers:
        featured_faqs = FAQ.objects.filter(
            is_active=True, 
            is_featured=True
        ).order_by('order')[:5]
    
    context = {
        'form': form,
        'services': services,
        'site_settings': site_settings,
        'quick_answers': quick_answers,
        'featured_faqs': featured_faqs,
    }
    
    return render(request, 'pages/contact.html', context)


@require_POST
def ajax_contact_view(request):
    """AJAX contact form submission"""
    form = ContactForm(request.POST)
    
    if form.is_valid():
        contact_message = form.save(commit=False)
        
        # Add metadata
        contact_message.ip_address = request.META.get('REMOTE_ADDR')
        contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        contact_message.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message! I\'ll get back to you soon.'
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


def search_view(request):
    """Global search view"""
    query = request.GET.get('q', '')
    
    if not query:
        return render(request, 'pages/search.html', {'query': query})
    
    # Search in projects
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(detailed_description__icontains=query),
        status__in=['published', 'featured']
    ).select_related('category')[:5]
    
    # Search in blog posts
    blog_posts = BlogPost.objects.filter(
        Q(title__icontains=query) |
        Q(excerpt__icontains=query) |
        Q(content__icontains=query),
        status__in=['published', 'featured']
    ).select_related('author', 'category')[:5]
    
    # Search in services
    services = Service.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(short_description__icontains=query),
        is_active=True
    )[:5]
    
    context = {
        'query': query,
        'projects': projects,
        'blog_posts': blog_posts,
        'services': services,
    }
    
    return render(request, 'pages/search.html', context)


def api_search_view(request):
    """API endpoint for AJAX search functionality"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({
            'success': False,
            'message': 'Query too short',
            'results': {}
        })
    
    # Search in projects
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(detailed_description__icontains=query),
        status__in=['published', 'featured']
    ).select_related('category').values(
        'title', 'slug', 'description', 'created_at'
    )[:5]
    
    # Search in blog posts
    blog_posts = BlogPost.objects.filter(
        Q(title__icontains=query) |
        Q(excerpt__icontains=query) |
        Q(content__icontains=query),
        status__in=['published', 'featured']
    ).select_related('category').values(
        'title', 'slug', 'excerpt', 'created_at'
    )[:5]
    
    # Search in services
    services = Service.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(short_description__icontains=query),
        is_active=True
    ).values(
        'name', 'slug', 'description', 'short_description'
    )[:5]
    
    # Format results for JSON response
    results = {
        'projects': [
            {
                'title': project['title'],
                'slug': project['slug'],
                'description': project['description'],
                'date': project['created_at'].strftime('%B %d, %Y') if project['created_at'] else ''
            }
            for project in projects
        ],
        'blog_posts': [
            {
                'title': post['title'],
                'slug': post['slug'],
                'excerpt': post['excerpt'] or '',
                'date': post['created_at'].strftime('%B %d, %Y') if post['created_at'] else ''
            }
            for post in blog_posts
        ],
        'services': [
            {
                'name': service['name'],
                'slug': service['slug'],
                'description': service['short_description'] or service['description']
            }
            for service in services
        ]
    }
    
    total_results = len(results['projects']) + len(results['blog_posts']) + len(results['services'])
    
    return JsonResponse({
        'success': True,
        'query': query,
        'total_results': total_results,
        'results': results
    })


def cv_preview_view(request):
    """Preview CV before downloading"""
    try:
        # Generate CV data for preview
        cv_service = CVGenerationService()
        cv_data = cv_service._get_cv_data()
        
        # Render the CV HTML template for preview
        context = {
            'cv_data': cv_data,
            'include_sections': ['header', 'summary', 'experience', 'education', 'skills', 'contact'],
            'generated_date': timezone.now().date(),
            'format_type': 'modern',
            'is_preview': True,
        }
        
        return render(request, 'cv/cv_preview.html', context)
        
    except Exception as e:
        # Log the error and return error page
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"CV preview failed: {e}")
        
        messages.error(request, f'Error generating CV preview: {str(e)}')
        return render(request, 'cv/cv_error.html', {'error': str(e)})


def download_cv_view(request):
    """Generate and download CV as PDF"""
    try:
        # Generate CV PDF - the service returns HttpResponse directly
        cv_service = CVGenerationService()
        return cv_service.generate_cv_pdf()
        
    except Exception as e:
        # Log the error and return a user-friendly message
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"CV generation failed: {e}")
        
        messages.error(request, f'Error generating CV: {str(e)}')
        return render(request, 'cv/cv_error.html', {'error': str(e)})

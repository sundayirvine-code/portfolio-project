from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from .models import Project, BlogPost, Testimonial, Service, ContactMessage, Category, Technology
from .forms import ContactForm
from .services import CVGenerationService


def home_view(request):
    """Home page view with featured content"""
    # Featured projects
    featured_projects = Project.objects.filter(
        status='featured'
    ).select_related('category').prefetch_related('technologies')[:4]
    
    # Recent blog posts
    recent_posts = BlogPost.objects.filter(
        status__in=['published', 'featured']
    ).select_related('author', 'category')[:3]
    
    # Featured testimonials
    featured_testimonials = Testimonial.objects.filter(
        is_featured=True, 
        is_approved=True
    ).select_related('project')[:3]
    
    # Featured services
    featured_services = Service.objects.filter(
        is_active=True, 
        is_featured=True
    ).prefetch_related('technologies')[:3]
    
    context = {
        'featured_projects': featured_projects,
        'recent_posts': recent_posts,
        'featured_testimonials': featured_testimonials,
        'featured_services': featured_services,
    }
    
    return render(request, 'pages/home.html', context)


def about_view(request):
    """About page view"""
    # Top technologies by proficiency
    top_technologies = Technology.objects.filter(
        proficiency__gte=70
    ).order_by('-proficiency', '-years_experience')[:10]
    
    # All technologies grouped by proficiency
    technologies = Technology.objects.all().order_by('-proficiency', 'name')
    
    context = {
        'top_technologies': top_technologies,
        'technologies': technologies,
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
    
    context = {
        'services': services,
        'expert_technologies': expert_technologies,
        'advanced_technologies': advanced_technologies,
        'intermediate_technologies': intermediate_technologies,
    }
    
    return render(request, 'pages/services.html', context)


def testimonials_view(request):
    """Testimonials view"""
    testimonials = Testimonial.objects.filter(
        is_approved=True
    ).select_related('project')
    
    # Pagination
    paginator = Paginator(testimonials, 6)  # 6 testimonials per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
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
    
    # Services for dropdown
    services = Service.objects.filter(is_active=True)
    
    context = {
        'form': form,
        'services': services,
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


def download_cv_view(request):
    """Generate and download CV as PDF"""
    try:
        # Generate CV PDF
        cv_service = CVGenerationService()
        pdf_content = cv_service.generate_cv_pdf()
        
        # Create HTTP response with PDF
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="CV.pdf"'
        response['Content-Length'] = len(pdf_content)
        
        return response
        
    except Exception as e:
        # Log the error and return a user-friendly message
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"CV generation failed: {e}")
        
        # Return a simple error response
        return HttpResponse(
            "Sorry, there was an error generating your CV. Please try again later.",
            status=500,
            content_type='text/plain'
        )

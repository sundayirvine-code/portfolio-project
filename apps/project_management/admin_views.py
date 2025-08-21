"""
Admin views for project management models
Comprehensive CRUD operations with proper pagination, search, and filtering
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Category, Technology, Project, BlogPost, Testimonial, Service, ContactMessage
from .admin_forms import (
    CategoryForm, TechnologyForm, ProjectForm, BlogPostForm, 
    TestimonialForm, ServiceForm, ContactMessageStatusForm,
    BulkDeleteForm, BulkStatusForm
)


# ===============================================================
# CATEGORY MANAGEMENT VIEWS
# ===============================================================

@staff_member_required
def category_list(request):
    """List all categories with search and pagination"""
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Add project and blog post counts
    categories = categories.annotate(
        project_count=Count('project'),
        blogpost_count=Count('blogpost')
    )
    
    # Pagination
    paginator = Paginator(categories, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'title': 'Category Management',
        'description': 'Manage project and blog categories'
    }
    
    return render(request, 'project_management/admin/category_list.html', context)


@staff_member_required
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('portfolio:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Create Category',
        'description': 'Add a new category for projects and blog posts',
        'form_action': 'Create'
    }
    
    return render(request, 'project_management/admin/category_form.html', context)


@staff_member_required
def category_edit(request, pk):
    """Edit existing category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('portfolio:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': f'Edit Category: {category.name}',
        'description': 'Update category information',
        'form_action': 'Update'
    }
    
    return render(request, 'project_management/admin/category_form.html', context)


@staff_member_required
@require_POST
def category_delete(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk)
    category_name = category.name
    category.delete()
    messages.success(request, f'Category "{category_name}" deleted successfully!')
    return redirect('portfolio:category_list')


# ===============================================================
# TECHNOLOGY MANAGEMENT VIEWS
# ===============================================================

@staff_member_required
def technology_list(request):
    """List all technologies with search and pagination"""
    technologies = Technology.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        technologies = technologies.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filtering by proficiency
    proficiency_filter = request.GET.get('proficiency', '')
    if proficiency_filter:
        if proficiency_filter == 'expert':
            technologies = technologies.filter(proficiency__gte=90)
        elif proficiency_filter == 'advanced':
            technologies = technologies.filter(proficiency__gte=70, proficiency__lt=90)
        elif proficiency_filter == 'intermediate':
            technologies = technologies.filter(proficiency__gte=50, proficiency__lt=70)
        elif proficiency_filter == 'beginner':
            technologies = technologies.filter(proficiency__lt=50)
    
    # Add project and service counts
    technologies = technologies.annotate(
        project_count=Count('project'),
        service_count=Count('service')
    )
    
    # Pagination
    paginator = Paginator(technologies, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'proficiency_filter': proficiency_filter,
        'title': 'Technology Management',
        'description': 'Manage technologies and skills'
    }
    
    return render(request, 'project_management/admin/technology_list.html', context)


@staff_member_required
def technology_create(request):
    """Create new technology"""
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            technology = form.save()
            messages.success(request, f'Technology "{technology.name}" created successfully!')
            return redirect('portfolio:technology_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TechnologyForm()
    
    context = {
        'form': form,
        'title': 'Create Technology',
        'description': 'Add a new technology or skill',
        'form_action': 'Create'
    }
    
    return render(request, 'project_management/admin/technology_form.html', context)


@staff_member_required
def technology_edit(request, pk):
    """Edit existing technology"""
    technology = get_object_or_404(Technology, pk=pk)
    
    if request.method == 'POST':
        form = TechnologyForm(request.POST, instance=technology)
        if form.is_valid():
            technology = form.save()
            messages.success(request, f'Technology "{technology.name}" updated successfully!')
            return redirect('portfolio:technology_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TechnologyForm(instance=technology)
    
    context = {
        'form': form,
        'technology': technology,
        'title': f'Edit Technology: {technology.name}',
        'description': 'Update technology information',
        'form_action': 'Update'
    }
    
    return render(request, 'project_management/admin/technology_form.html', context)


@staff_member_required
@require_POST
def technology_delete(request, pk):
    """Delete technology"""
    technology = get_object_or_404(Technology, pk=pk)
    technology_name = technology.name
    technology.delete()
    messages.success(request, f'Technology "{technology_name}" deleted successfully!')
    return redirect('portfolio:technology_list')


# ===============================================================
# PROJECT MANAGEMENT VIEWS
# ===============================================================

@staff_member_required
def project_list_admin(request):
    """List all projects with search, filtering, and pagination"""
    projects = Project.objects.select_related('category').prefetch_related('technologies')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(client__icontains=search_query)
        )
    
    # Status filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # Category filtering
    category_filter = request.GET.get('category', '')
    if category_filter:
        projects = projects.filter(category_id=category_filter)
    
    # Project type filtering
    type_filter = request.GET.get('type', '')
    if type_filter:
        projects = projects.filter(project_type=type_filter)
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'type_filter': type_filter,
        'categories': categories,
        'project_statuses': Project.STATUS_CHOICES,
        'project_types': Project.TYPE_CHOICES,
        'title': 'Project Management',
        'description': 'Manage portfolio projects'
    }
    
    return render(request, 'project_management/admin/project_list.html', context)


@staff_member_required
def project_create_admin(request):
    """Create new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.title}" created successfully!')
            return redirect('portfolio:project_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()
    
    context = {
        'form': form,
        'title': 'Create Project',
        'description': 'Add a new portfolio project',
        'form_action': 'Create'
    }
    
    return render(request, 'project_management/admin/project_form.html', context)


@staff_member_required
def project_edit_admin(request, pk):
    """Edit existing project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.title}" updated successfully!')
            return redirect('portfolio:project_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
        'title': f'Edit Project: {project.title}',
        'description': 'Update project information',
        'form_action': 'Update'
    }
    
    return render(request, 'project_management/admin/project_form.html', context)


@staff_member_required
@require_POST
def project_delete_admin(request, pk):
    """Delete project"""
    project = get_object_or_404(Project, pk=pk)
    project_title = project.title
    project.delete()
    messages.success(request, f'Project "{project_title}" deleted successfully!')
    return redirect('portfolio:project_list')


# ===============================================================
# BLOG POST MANAGEMENT VIEWS
# ===============================================================

@staff_member_required
def blogpost_list(request):
    """List all blog posts with search, filtering, and pagination"""
    blog_posts = BlogPost.objects.select_related('author', 'category')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        blog_posts = blog_posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Status filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        blog_posts = blog_posts.filter(status=status_filter)
    
    # Category filtering
    category_filter = request.GET.get('category', '')
    if category_filter:
        blog_posts = blog_posts.filter(category_id=category_filter)
    
    # Pagination
    paginator = Paginator(blog_posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'categories': categories,
        'blog_statuses': BlogPost.STATUS_CHOICES,
        'title': 'Blog Post Management',
        'description': 'Manage blog posts and articles'
    }
    
    return render(request, 'project_management/admin/blogpost_list.html', context)


@staff_member_required
def blogpost_create(request):
    """Create new blog post"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, f'Blog post "{blog_post.title}" created successfully!')
            return redirect('portfolio:blogpost_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm()
    
    context = {
        'form': form,
        'title': 'Create Blog Post',
        'description': 'Write a new blog post or article',
        'form_action': 'Create'
    }
    
    return render(request, 'project_management/admin/blogpost_form.html', context)


@staff_member_required
def blogpost_edit(request, pk):
    """Edit existing blog post"""
    blog_post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            blog_post = form.save()
            messages.success(request, f'Blog post "{blog_post.title}" updated successfully!')
            return redirect('portfolio:blogpost_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm(instance=blog_post)
    
    context = {
        'form': form,
        'blog_post': blog_post,
        'title': f'Edit Blog Post: {blog_post.title}',
        'description': 'Update blog post content',
        'form_action': 'Update'
    }
    
    return render(request, 'project_management/admin/blogpost_form.html', context)


@staff_member_required
@require_POST
def blogpost_delete(request, pk):
    """Delete blog post"""
    blog_post = get_object_or_404(BlogPost, pk=pk)
    blog_post_title = blog_post.title
    blog_post.delete()
    messages.success(request, f'Blog post "{blog_post_title}" deleted successfully!')
    return redirect('portfolio:blogpost_list')


# ===============================================================
# TESTIMONIAL MANAGEMENT VIEWS
# ===============================================================

@staff_member_required
def testimonial_list(request):
    """List all testimonials with search, filtering, and pagination"""
    testimonials = Testimonial.objects.select_related('project')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        testimonials = testimonials.filter(
            Q(client_name__icontains=search_query) |
            Q(client_company__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Approval filtering
    approval_filter = request.GET.get('approval', '')
    if approval_filter:
        if approval_filter == 'approved':
            testimonials = testimonials.filter(is_approved=True)
        elif approval_filter == 'pending':
            testimonials = testimonials.filter(is_approved=False)
    
    # Featured filtering
    featured_filter = request.GET.get('featured', '')
    if featured_filter:
        if featured_filter == 'featured':
            testimonials = testimonials.filter(is_featured=True)
        elif featured_filter == 'not_featured':
            testimonials = testimonials.filter(is_featured=False)
    
    # Rating filtering
    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        testimonials = testimonials.filter(rating=rating_filter)
    
    # Pagination
    paginator = Paginator(testimonials, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'approval_filter': approval_filter,
        'featured_filter': featured_filter,
        'rating_filter': rating_filter,
        'title': 'Testimonial Management',
        'description': 'Manage client testimonials and reviews'
    }
    
    return render(request, 'project_management/admin/testimonial_list.html', context)


@staff_member_required
def testimonial_create(request):
    """Create new testimonial"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save()
            messages.success(request, f'Testimonial from "{testimonial.client_name}" created successfully!')
            return redirect('portfolio:testimonial_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TestimonialForm()
    
    context = {
        'form': form,
        'title': 'Create Testimonial',
        'description': 'Add a new client testimonial',
        'form_action': 'Create'
    }
    
    return render(request, 'project_management/admin/testimonial_form.html', context)


@staff_member_required
def testimonial_edit(request, pk):
    """Edit existing testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            testimonial = form.save()
            messages.success(request, f'Testimonial from "{testimonial.client_name}" updated successfully!')
            return redirect('portfolio:testimonial_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TestimonialForm(instance=testimonial)
    
    context = {
        'form': form,
        'testimonial': testimonial,
        'title': f'Edit Testimonial: {testimonial.client_name}',
        'description': 'Update testimonial information',
        'form_action': 'Update'
    }
    
    return render(request, 'project_management/admin/testimonial_form.html', context)


@staff_member_required
@require_POST
def testimonial_delete(request, pk):
    """Delete testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    client_name = testimonial.client_name
    testimonial.delete()
    messages.success(request, f'Testimonial from "{client_name}" deleted successfully!')
    return redirect('portfolio:testimonial_list')


# ===============================================================
# SERVICE MANAGEMENT VIEWS
# ===============================================================

@staff_member_required
def service_list_admin(request):
    """List all services with search, filtering, and pagination"""
    services = Service.objects.prefetch_related('technologies')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Active filtering
    active_filter = request.GET.get('active', '')
    if active_filter:
        if active_filter == 'active':
            services = services.filter(is_active=True)
        elif active_filter == 'inactive':
            services = services.filter(is_active=False)
    
    # Featured filtering
    featured_filter = request.GET.get('featured', '')
    if featured_filter:
        if featured_filter == 'featured':
            services = services.filter(is_featured=True)
        elif featured_filter == 'not_featured':
            services = services.filter(is_featured=False)
    
    # Pagination
    paginator = Paginator(services, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'active_filter': active_filter,
        'featured_filter': featured_filter,
        'title': 'Service Management',
        'description': 'Manage services and offerings'
    }
    
    return render(request, 'project_management/admin/service_list.html', context)


@staff_member_required
def service_create_admin(request):
    """Create new service"""
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            messages.success(request, f'Service "{service.name}" created successfully!')
            return redirect('portfolio:service_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()
    
    context = {
        'form': form,
        'title': 'Create Service',
        'description': 'Add a new service offering',
        'form_action': 'Create'
    }
    
    return render(request, 'project_management/admin/service_form.html', context)


@staff_member_required
def service_edit_admin(request, pk):
    """Edit existing service"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            messages.success(request, f'Service "{service.name}" updated successfully!')
            return redirect('portfolio:service_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm(instance=service)
    
    context = {
        'form': form,
        'service': service,
        'title': f'Edit Service: {service.name}',
        'description': 'Update service information',
        'form_action': 'Update'
    }
    
    return render(request, 'project_management/admin/service_form.html', context)


@staff_member_required
@require_POST
def service_delete_admin(request, pk):
    """Delete service"""
    service = get_object_or_404(Service, pk=pk)
    service_name = service.name
    service.delete()
    messages.success(request, f'Service "{service_name}" deleted successfully!')
    return redirect('portfolio:service_list')


# ===============================================================
# CONTACT MESSAGE VIEWS
# ===============================================================

@staff_member_required
def contact_messages(request):
    """List all contact messages with search, filtering, and pagination"""
    messages_queryset = ContactMessage.objects.select_related('service_interest')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        messages_queryset = messages_queryset.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    
    # Status filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        messages_queryset = messages_queryset.filter(status=status_filter)
    
    # Service filtering
    service_filter = request.GET.get('service', '')
    if service_filter:
        messages_queryset = messages_queryset.filter(service_interest_id=service_filter)
    
    # Pagination
    paginator = Paginator(messages_queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    services = Service.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'service_filter': service_filter,
        'services': services,
        'message_statuses': ContactMessage.STATUS_CHOICES,
        'title': 'Contact Messages',
        'description': 'View and manage contact form submissions'
    }
    
    return render(request, 'project_management/admin/contact_messages.html', context)


@staff_member_required
def contact_message_detail(request, pk):
    """View contact message details and update status"""
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    
    if request.method == 'POST':
        form = ContactMessageStatusForm(request.POST, instance=contact_message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message status updated successfully!')
            return redirect('portfolio:contact_messages')
    else:
        form = ContactMessageStatusForm(instance=contact_message)
    
    context = {
        'contact_message': contact_message,
        'form': form,
        'title': f'Message from {contact_message.name}',
        'description': 'View contact message details and update status'
    }
    
    return render(request, 'project_management/admin/contact_message_detail.html', context)


@staff_member_required
@require_POST
def contact_message_delete(request, pk):
    """Delete contact message"""
    contact_message = get_object_or_404(ContactMessage, pk=pk)
    sender_name = contact_message.name
    contact_message.delete()
    messages.success(request, f'Message from "{sender_name}" deleted successfully!')
    return redirect('portfolio:contact_messages')


# ===============================================================
# BULK OPERATIONS
# ===============================================================


@staff_member_required
@require_POST
def bulk_status_update(request):
    """Handle bulk status updates"""
    form = BulkStatusForm(request.POST)
    if form.is_valid():
        item_ids = form.cleaned_data['selected_items']
        new_status = form.cleaned_data['new_status']
        model_type = request.POST.get('model_type')
        
        count = 0
        if model_type == 'project':
            count = Project.objects.filter(id__in=item_ids).update(status=new_status)
        elif model_type == 'blogpost':
            count = BlogPost.objects.filter(id__in=item_ids).update(status=new_status)
        elif model_type == 'contact_message':
            count = ContactMessage.objects.filter(id__in=item_ids).update(status=new_status)
        
        messages.success(request, f'Successfully updated status for {count} items.')
    else:
        messages.error(request, 'Invalid selection for bulk update.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required
@require_POST
def bulk_delete(request):
    """Handle bulk delete operations"""
    form = BulkDeleteForm(request.POST)
    if form.is_valid():
        item_ids = form.cleaned_data['selected_items']
        model_type = request.POST.get('model_type')
        
        count = 0
        if model_type == 'project':
            count = Project.objects.filter(id__in=item_ids).count()
            Project.objects.filter(id__in=item_ids).delete()
        elif model_type == 'blogpost':
            count = BlogPost.objects.filter(id__in=item_ids).count()
            BlogPost.objects.filter(id__in=item_ids).delete()
        elif model_type == 'testimonial':
            count = Testimonial.objects.filter(id__in=item_ids).count()
            Testimonial.objects.filter(id__in=item_ids).delete()
        elif model_type == 'service':
            count = Service.objects.filter(id__in=item_ids).count()
            Service.objects.filter(id__in=item_ids).delete()
        elif model_type == 'category':
            count = Category.objects.filter(id__in=item_ids).count()
            Category.objects.filter(id__in=item_ids).delete()
        elif model_type == 'technology':
            count = Technology.objects.filter(id__in=item_ids).count()
            Technology.objects.filter(id__in=item_ids).delete()
        elif model_type == 'contact_message':
            count = ContactMessage.objects.filter(id__in=item_ids).count()
            ContactMessage.objects.filter(id__in=item_ids).delete()
        
        messages.success(request, f'Successfully deleted {count} items.')
    else:
        messages.error(request, 'Invalid selection for bulk delete.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count
from .models import Project, BlogPost, Technology, Category, Service, ContactMessage
from .serializers import (
    ProjectSerializer, BlogPostSerializer, TechnologySerializer,
    CategorySerializer, ServiceSerializer, ContactMessageSerializer
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for projects"""
    
    queryset = Project.objects.filter(status__in=['published', 'featured']).select_related('category').prefetch_related('technologies')
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by technology
        technology = self.request.query_params.get('technology')
        if technology:
            queryset = queryset.filter(technologies__slug=technology)
        
        # Filter by project type
        project_type = self.request.query_params.get('type')
        if project_type:
            queryset = queryset.filter(project_type=project_type)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured projects"""
        featured_projects = self.queryset.filter(status='featured')[:6]
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for blog posts"""
    
    queryset = BlogPost.objects.filter(status__in=['published', 'featured']).select_related('author', 'category')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by tag
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent blog posts"""
        recent_posts = self.queryset[:5]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for technologies"""
    
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    lookup_field = 'slug'
    
    @action(detail=False, methods=['get'])
    def top_skills(self, request):
        """Get top technologies by proficiency"""
        top_technologies = self.queryset.filter(proficiency__gte=70).order_by('-proficiency')[:10]
        serializer = self.get_serializer(top_technologies, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for categories"""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for services"""
    
    queryset = Service.objects.filter(is_active=True).prefetch_related('technologies')
    serializer_class = ServiceSerializer
    lookup_field = 'slug'
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured services"""
        featured_services = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_services, many=True)
        return Response(serializer.data)


class ContactAPIView(APIView):
    """API view for contact form submission"""
    
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        
        if serializer.is_valid():
            contact_message = serializer.save()
            
            # Add metadata
            contact_message.ip_address = request.META.get('REMOTE_ADDR')
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            
            return Response({
                'success': True,
                'message': 'Thank you for your message! I\'ll get back to you soon.'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class StatsAPIView(APIView):
    """API view for portfolio statistics"""
    
    def get(self, request):
        # Calculate portfolio statistics
        stats = {
            'total_projects': Project.objects.filter(status__in=['published', 'featured']).count(),
            'total_blog_posts': BlogPost.objects.filter(status__in=['published', 'featured']).count(),
            'total_technologies': Technology.objects.count(),
            'total_services': Service.objects.filter(is_active=True).count(),
            'featured_projects': Project.objects.filter(status='featured').count(),
            'project_types': list(Project.objects.filter(
                status__in=['published', 'featured']
            ).values('project_type').annotate(count=Count('project_type'))),
            'top_technologies': list(Technology.objects.filter(
                proficiency__gte=80
            ).values('name', 'proficiency', 'years_experience')[:10]),
        }
        
        return Response(stats)
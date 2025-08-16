from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create router for API viewsets
router = DefaultRouter()
router.register(r'projects', api_views.ProjectViewSet)
router.register(r'blog-posts', api_views.BlogPostViewSet)
router.register(r'technologies', api_views.TechnologyViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'services', api_views.ServiceViewSet)

app_name = 'api'

urlpatterns = [
    # ViewSet URLs
    path('', include(router.urls)),
    
    # Custom endpoints
    path('contact/', api_views.ContactAPIView.as_view(), name='contact'),
    path('stats/', api_views.StatsAPIView.as_view(), name='stats'),
]
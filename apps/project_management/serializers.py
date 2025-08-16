from rest_framework import serializers
from .models import Project, BlogPost, Technology, Category, Service, ContactMessage, Testimonial


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color', 'icon']


class TechnologySerializer(serializers.ModelSerializer):
    """Serializer for Technology model"""
    
    class Meta:
        model = Technology
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 
            'website_url', 'proficiency', 'years_experience'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    
    category = CategorySerializer(read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)
    duration_months = serializers.ReadOnlyField()
    is_published = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'detailed_description',
            'project_type', 'status', 'category', 'technologies',
            'featured_image', 'live_url', 'github_url', 'documentation_url',
            'start_date', 'end_date', 'client', 'team_size',
            'duration_months', 'is_published', 'created_at', 'updated_at'
        ]


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""
    
    author = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tag_list = serializers.ReadOnlyField()
    is_published = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content',
            'author', 'category', 'tags', 'tag_list', 'status',
            'featured_image', 'views_count', 'is_published',
            'published_at', 'created_at', 'updated_at'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model"""
    
    technologies = TechnologySerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'icon', 'technologies', 'starting_price', 'price_unit',
            'is_active', 'is_featured', 'order'
        ]


class TestimonialSerializer(serializers.ModelSerializer):
    """Serializer for Testimonial model"""
    
    project = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'client_position', 'client_company',
            'client_photo', 'content', 'rating', 'project',
            'is_featured', 'created_at'
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'name', 'email', 'phone', 'company',
            'subject', 'message', 'service_interest'
        ]
        
    def validate_email(self):
        """Custom email validation"""
        email = self.initial_data.get('email')
        if not email:
            raise serializers.ValidationError("Email is required.")
        return email
    
    def validate_message(self):
        """Custom message validation"""
        message = self.initial_data.get('message')
        if message and len(message) < 10:
            raise serializers.ValidationError("Please provide a more detailed message (at least 10 characters).")
        return message
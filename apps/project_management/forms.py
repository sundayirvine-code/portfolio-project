from django import forms
from django.core.validators import EmailValidator
from .models import ContactMessage, Service


class ContactForm(forms.ModelForm):
    """Contact form for the contact page"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message', 'service_interest']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize form widgets and attributes
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your Full Name *',
            'required': True
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'your.email@example.com *',
            'required': True,
            'type': 'email'
        })
        
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '+1 (555) 123-4567',
            'type': 'tel'
        })
        
        self.fields['company'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your Company (Optional)'
        })
        
        self.fields['subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Brief subject of your message *',
            'required': True
        })
        
        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tell me about your project, requirements, or question...',
            'rows': 5,
            'required': True
        })
        
        self.fields['service_interest'].widget.attrs.update({
            'class': 'form-select'
        })
        
        # Set service interest choices
        self.fields['service_interest'].queryset = Service.objects.filter(is_active=True)
        self.fields['service_interest'].empty_label = "Select a service (Optional)"
        
    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            validator(email)
        return email
    
    def clean_name(self):
        """Validate and clean name field"""
        name = self.cleaned_data.get('name')
        if name:
            # Remove extra whitespace and capitalize properly
            name = ' '.join(word.capitalize() for word in name.split())
        return name
    
    def clean_message(self):
        """Validate message length"""
        message = self.cleaned_data.get('message')
        if message and len(message) < 10:
            raise forms.ValidationError("Please provide a more detailed message (at least 10 characters).")
        return message
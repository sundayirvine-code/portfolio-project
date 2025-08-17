from django import forms
from django.utils.safestring import mark_safe
import base64


class ImagePickerWidget(forms.Textarea):
    """
    Custom widget that combines file input with base64 textarea for image handling
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control d-none',
            'rows': 3,
            'placeholder': 'Base64 image data will appear here...'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # Get the standard textarea
        textarea = super().render(name, value, attrs, renderer)
        
        # Create the file input and preview elements
        widget_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'
        
        html = f'''
        <div class="image-picker-container" data-widget-id="{widget_id}">
            <!-- File Input -->
            <div class="mb-3">
                <label class="form-label">Choose Image</label>
                <input type="file" 
                       class="form-control image-file-input" 
                       accept="image/*"
                       data-target="{widget_id}">
                <div class="form-text">
                    Select an image file. It will be automatically converted to Base64 format.
                    Recommended: JPG, PNG, WebP. Max size: 2MB.
                </div>
            </div>
            
            <!-- Image Preview -->
            <div class="image-preview-container mb-3" style="display: none;">
                <label class="form-label">Preview</label>
                <div class="border rounded p-2 text-center bg-light" style="min-height: 150px;">
                    <img class="image-preview" 
                         style="max-width: 100%; max-height: 200px; object-fit: contain;" 
                         alt="Image preview">
                </div>
                <div class="mt-2">
                    <button type="button" class="btn btn-sm btn-outline-danger remove-image">
                        <i class="bi bi-trash"></i> Remove Image
                    </button>
                </div>
            </div>
            
            <!-- Base64 Textarea (hidden by default) -->
            <div class="base64-container">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <label class="form-label mb-0">Base64 Data</label>
                    <button type="button" class="btn btn-sm btn-outline-secondary toggle-base64">
                        <i class="bi bi-code"></i> Show/Hide
                    </button>
                </div>
                {textarea}
            </div>
        </div>
        '''
        
        return mark_safe(html)
    
    class Media:
        js = ('js/image-picker.js',)
        css = {
            'all': ('css/image-picker.css',)
        }


class Base64ImageField(forms.CharField):
    """
    Custom form field for handling Base64 encoded images
    """
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', ImagePickerWidget())
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)
    
    def validate(self, value):
        super().validate(value)
        
        if value and not self.is_valid_base64_image(value):
            raise forms.ValidationError("Invalid image data. Please select a valid image file.")
    
    def is_valid_base64_image(self, value):
        """
        Validate that the value is a proper base64 encoded image
        """
        if not value:
            return True
        
        try:
            # Check if it starts with data URL prefix
            if value.startswith('data:image/'):
                # Extract the base64 part
                header, data = value.split(',', 1)
                base64.b64decode(data)
                return True
            else:
                # Try to decode as raw base64
                base64.b64decode(value)
                return True
        except (ValueError, TypeError):
            return False
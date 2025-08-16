from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Base64ImageWidget(forms.Widget):
    """Widget for handling base64 image uploads"""
    
    template_name = 'admin/widgets/base64_image_widget.html'
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'base64-image-input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        """Format the value for display"""
        if value and isinstance(value, str):
            if value.startswith('data:image'):
                return value
            elif value:
                return f"data:image/jpeg;base64,{value}"
        return value
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget"""
        if attrs is None:
            attrs = {}
        
        # File input for new uploads
        file_input = forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'onchange': f'handleImageUpload(this, "{name}")'
        }).render(f'{name}_file', None, attrs)
        
        # Hidden input for base64 data
        hidden_input = forms.HiddenInput().render(name, value, attrs)
        
        # Image preview
        preview_html = ''
        if value:
            formatted_value = self.format_value(value)
            preview_html = format_html(
                '<div class="image-preview mb-2"><img src="{}" style="max-width: 200px; max-height: 200px;" class="img-thumbnail"></div>',
                formatted_value
            )
        
        # Clear button
        clear_button = ''
        if value:
            clear_button = format_html(
                '<button type="button" class="btn btn-sm btn-outline-danger mb-2" onclick="clearImage(\'{}\')">Clear Image</button>',
                name
            )
        
        return mark_safe(f'''
            <div class="base64-image-widget">
                {preview_html}
                {file_input}
                {clear_button}
                {hidden_input}
            </div>
        ''')
    
    class Media:
        js = ('admin/js/base64_image_widget.js',)
        css = {
            'all': ('admin/css/base64_image_widget.css',)
        }


class MultipleBase64ImageWidget(forms.Widget):
    """Widget for handling multiple base64 image uploads"""
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'multiple-base64-image-input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        """Format the value for display"""
        if value:
            try:
                import json
                images = json.loads(value) if isinstance(value, str) else value
                return images if isinstance(images, list) else []
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget"""
        if attrs is None:
            attrs = {}
        
        # File input for new uploads (multiple)
        file_input = forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'multiple': True,
            'onchange': f'handleMultipleImageUpload(this, "{name}")'
        }).render(f'{name}_files', None, attrs)
        
        # Hidden input for JSON data
        hidden_input = forms.HiddenInput().render(name, value, attrs)
        
        # Images preview
        images = self.format_value(value)
        preview_html = '<div class="gallery-preview row">'
        
        for i, img_data in enumerate(images):
            formatted_img = img_data if img_data.startswith('data:image') else f"data:image/jpeg;base64,{img_data}"
            preview_html += format_html(
                '''<div class="col-md-3 mb-2">
                    <div class="card">
                        <img src="{}" class="card-img-top" style="height: 150px; object-fit: cover;">
                        <div class="card-body p-2">
                            <button type="button" class="btn btn-sm btn-outline-danger w-100" 
                                    onclick="removeGalleryImage('{}', {})">Remove</button>
                        </div>
                    </div>
                </div>''',
                formatted_img, name, i
            )
        
        preview_html += '</div>'
        
        return mark_safe(f'''
            <div class="multiple-base64-image-widget">
                {preview_html}
                {file_input}
                {hidden_input}
            </div>
        ''')
    
    class Media:
        js = ('admin/js/multiple_base64_image_widget.js',)
        css = {
            'all': ('admin/css/base64_image_widget.css',)
        }
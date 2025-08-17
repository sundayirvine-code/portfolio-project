"""
User-friendly forms for managing JSON fields in Site Parameters
"""
from django import forms
import json


class FunFactForm(forms.Form):
    """Form for a single fun fact entry"""
    label = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Cups of Coffee'
        })
    )
    value = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 500',
            'min': 0
        })
    )
    color = forms.ChoiceField(
        choices=[
            ('primary', 'Blue'),
            ('success', 'Green'), 
            ('warning', 'Yellow'),
            ('danger', 'Red'),
            ('info', 'Cyan'),
            ('secondary', 'Gray')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class ValueForm(forms.Form):
    """Form for a single value entry"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Innovation'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Brief description of this value'
        })
    )
    icon = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., lightbulb (Bootstrap icon name)'
        }),
        help_text="Bootstrap icon name without 'bi bi-' prefix"
    )
    color = forms.ChoiceField(
        choices=[
            ('primary', 'Blue'),
            ('success', 'Green'), 
            ('warning', 'Yellow'),
            ('danger', 'Red'),
            ('info', 'Cyan'),
            ('secondary', 'Gray')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class InterestForm(forms.Form):
    """Form for a single interest entry"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Web Development'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Brief description of this interest'
        }),
        required=False
    )


class FunFactsManagerForm(forms.Form):
    """Form for managing multiple fun facts"""
    
    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop('initial_data', [])
        super().__init__(*args, **kwargs)
        
        # Add fields dynamically based on initial data
        for i, fact in enumerate(initial_data):
            self.fields[f'fact_{i}_label'] = forms.CharField(
                initial=fact.get('label', ''),
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g., Cups of Coffee'
                })
            )
            self.fields[f'fact_{i}_value'] = forms.IntegerField(
                initial=fact.get('value', 0),
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g., 500',
                    'min': 0
                })
            )
            self.fields[f'fact_{i}_color'] = forms.ChoiceField(
                initial=fact.get('color', 'primary'),
                choices=[
                    ('primary', 'Blue'),
                    ('success', 'Green'), 
                    ('warning', 'Yellow'),
                    ('danger', 'Red'),
                    ('info', 'Cyan'),
                    ('secondary', 'Gray')
                ],
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            
    def get_facts_data(self):
        """Extract fun facts data from form"""
        facts = []
        i = 0
        while f'fact_{i}_label' in self.cleaned_data:
            if self.cleaned_data[f'fact_{i}_label']:  # Only include non-empty facts
                facts.append({
                    'label': self.cleaned_data[f'fact_{i}_label'],
                    'value': self.cleaned_data[f'fact_{i}_value'],
                    'color': self.cleaned_data[f'fact_{i}_color']
                })
            i += 1
        return facts


class ValuesManagerForm(forms.Form):
    """Form for managing values and interests"""
    
    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop('initial_data', {})
        super().__init__(*args, **kwargs)
        
        values = initial_data.get('values', [])
        interests = initial_data.get('interests', [])
        
        # Add value fields dynamically
        for i, value in enumerate(values):
            self.fields[f'value_{i}_name'] = forms.CharField(
                initial=value.get('name', ''),
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g., Innovation'
                })
            )
            self.fields[f'value_{i}_description'] = forms.CharField(
                initial=value.get('description', ''),
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'placeholder': 'Brief description'
                })
            )
            self.fields[f'value_{i}_icon'] = forms.CharField(
                initial=value.get('icon', ''),
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g., lightbulb'
                })
            )
            self.fields[f'value_{i}_color'] = forms.ChoiceField(
                initial=value.get('color', 'primary'),
                choices=[
                    ('primary', 'Blue'),
                    ('success', 'Green'), 
                    ('warning', 'Yellow'),
                    ('danger', 'Red'),
                    ('info', 'Cyan'),
                    ('secondary', 'Gray')
                ],
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            
        # Add interest fields dynamically  
        for i, interest in enumerate(interests):
            self.fields[f'interest_{i}_name'] = forms.CharField(
                initial=interest.get('name', ''),
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g., Web Development'
                })
            )
            self.fields[f'interest_{i}_description'] = forms.CharField(
                initial=interest.get('description', ''),
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'placeholder': 'Brief description'
                }),
                required=False
            )
            
    def get_values_interests_data(self):
        """Extract values and interests data from form"""
        values = []
        interests = []
        
        # Extract values
        i = 0
        while f'value_{i}_name' in self.cleaned_data:
            if self.cleaned_data[f'value_{i}_name']:  # Only include non-empty values
                values.append({
                    'name': self.cleaned_data[f'value_{i}_name'],
                    'description': self.cleaned_data[f'value_{i}_description'],
                    'icon': self.cleaned_data[f'value_{i}_icon'],
                    'color': self.cleaned_data[f'value_{i}_color']
                })
            i += 1
            
        # Extract interests
        i = 0
        while f'interest_{i}_name' in self.cleaned_data:
            if self.cleaned_data[f'interest_{i}_name']:  # Only include non-empty interests
                interests.append({
                    'name': self.cleaned_data[f'interest_{i}_name'],
                    'description': self.cleaned_data[f'interest_{i}_description']
                })
            i += 1
            
        return {
            'values': values,
            'interests': interests
        }
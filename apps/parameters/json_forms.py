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
    """Form for managing fun facts with JSON field support"""
    
    facts_data = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'display: none;',  # Hidden field for JSON data
        }),
        required=False,
        initial='[]'
    )
    
    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop('initial_data', [])
        super().__init__(*args, **kwargs)
        
        # Ensure we have a list format
        if not isinstance(initial_data, list):
            initial_data = []
        
        # Set initial JSON data
        if initial_data:
            import json
            self.fields['facts_data'].initial = json.dumps(initial_data)
    
    def clean_facts_data(self):
        """Validate and clean the JSON facts data"""
        import json
        data = self.cleaned_data.get('facts_data', '[]')
        
        try:
            facts_list = json.loads(data) if data else []
            
            # Validate each fact entry
            cleaned_facts = []
            for fact in facts_list:
                if not isinstance(fact, dict):
                    continue
                
                label = fact.get('label', '').strip()
                if not label:
                    continue  # Skip entries without labels
                
                try:
                    value = int(fact.get('value', 0))
                except (ValueError, TypeError):
                    value = 0
                
                cleaned_fact = {
                    'label': label,
                    'value': value,
                    'color': fact.get('color', 'primary'),
                    'icon': fact.get('icon', '').strip() or 'star'
                }
                cleaned_facts.append(cleaned_fact)
            
            return cleaned_facts
            
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON data for fun facts")
            
    def get_facts_data(self):
        """Get the cleaned fun facts data"""
        return self.cleaned_data.get('facts_data', [])


class ValuesManagerForm(forms.Form):
    """Form for managing values and interests with JSON field support"""
    
    values_data = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'display: none;',  # Hidden field for JSON data
        }),
        required=False,
        initial='[]'
    )
    
    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop('initial_data', [])
        super().__init__(*args, **kwargs)
        
        # Handle both legacy dict format and new list format
        if isinstance(initial_data, dict):
            # Legacy format: {'values': [...], 'interests': [...]}
            legacy_values = initial_data.get('values', [])
            legacy_interests = initial_data.get('interests', [])
            
            # Convert to new format
            converted_data = []
            for value in legacy_values:
                if isinstance(value, str):
                    converted_data.append({
                        'name': value,
                        'description': '',
                        'icon': 'heart',
                        'color': 'primary'
                    })
                elif isinstance(value, dict):
                    converted_data.append(value)
                    
            for interest in legacy_interests:
                if isinstance(interest, str):
                    converted_data.append({
                        'name': interest,
                        'description': '',
                        'icon': 'star',
                        'color': 'info'
                    })
                elif isinstance(interest, dict):
                    converted_data.append(interest)
            
            initial_data = converted_data
        elif not isinstance(initial_data, list):
            initial_data = []
        
        # Set initial JSON data
        if initial_data:
            import json
            self.fields['values_data'].initial = json.dumps(initial_data)
    
    def clean_values_data(self):
        """Validate and clean the JSON values data"""
        import json
        data = self.cleaned_data.get('values_data', '[]')
        
        try:
            values_list = json.loads(data) if data else []
            
            # Validate each value entry
            cleaned_values = []
            for value in values_list:
                if not isinstance(value, dict):
                    continue
                
                name = value.get('name', '').strip()
                if not name:
                    continue  # Skip entries without names
                
                cleaned_value = {
                    'name': name,
                    'description': value.get('description', '').strip(),
                    'icon': value.get('icon', '').strip() or 'star',
                    'color': value.get('color', 'primary')
                }
                cleaned_values.append(cleaned_value)
            
            return cleaned_values
            
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON data for values and interests")
            
    def get_values_interests_data(self):
        """Get the cleaned values and interests data"""
        return self.cleaned_data.get('values_data', [])


class SkillsManagerForm(forms.Form):
    """Form for managing skills and expertise with JSON field support"""
    
    skills_data = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'display: none;',  # Hidden field for JSON data
        }),
        required=False,
        initial='[]'
    )
    
    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop('initial_data', [])
        super().__init__(*args, **kwargs)
        
        # Ensure we have a list format
        if not isinstance(initial_data, list):
            initial_data = []
        
        # Set initial JSON data
        if initial_data:
            import json
            self.fields['skills_data'].initial = json.dumps(initial_data)
    
    def clean_skills_data(self):
        """Validate and clean the JSON skills data"""
        import json
        data = self.cleaned_data.get('skills_data', '[]')
        
        try:
            skills_list = json.loads(data) if data else []
            
            # Validate each skill entry
            cleaned_skills = []
            for skill in skills_list:
                if not isinstance(skill, dict):
                    continue
                
                name = skill.get('name', '').strip()
                if not name:
                    continue  # Skip entries without names
                
                # Validate level is between 0-100
                try:
                    level = int(skill.get('level', 0))
                    if level < 0:
                        level = 0
                    elif level > 100:
                        level = 100
                except (ValueError, TypeError):
                    level = 0
                
                cleaned_skill = {
                    'name': name,
                    'category': skill.get('category', '').strip() or 'other',
                    'level': level,
                    'icon': skill.get('icon', '').strip() or 'gear',
                    'color': skill.get('color', 'primary'),
                    'description': skill.get('description', '').strip()
                }
                cleaned_skills.append(cleaned_skill)
            
            return cleaned_skills
            
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON data for skills and expertise")
            
    def get_skills_data(self):
        """Get the cleaned skills data"""
        return self.cleaned_data.get('skills_data', [])
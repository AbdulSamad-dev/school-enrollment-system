from django import forms
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_appointment': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_school_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_school_leaving': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # Widget for image upload

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply a class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Optionally, set placeholders dynamically based on verbose_name
            field.widget.attrs['placeholder'] = field.label

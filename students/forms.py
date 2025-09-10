from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'GR_no',
            'seat_no',
            'date_of_admission',
            'admission_class',
            'current_class',
            'section',
            'medium',
            'gender',
            'religion',
            'name',
            'father_name',
            'caste',
            'date_of_birth',
            'place_of_birth',
            'district_of_birth',
            'taluka_of_birth',
            'previous_school',
            'previous_school_GR_no',
            'date_of_school_leaving',
            'last_class_studied',
            'reason_of_school_leaving',
            'exam_type',
            'exam_year',
            'exam_month',
            'grade',
            'progress',
            'conduct',
            'remarks',
            'parent_cnic',
            'cell_no',
            'nadra_id',
            'image',
        ]
        widgets = {
            'GR_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GR No'}),
            'seat_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seat No'}),
            'date_of_admission': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'admission_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admission Class'}),
            'current_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Class'}),
            'section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Section'}),
            'medium': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Father Name'}),
            'caste': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Caste'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place of Birth'}),
            'district_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District of Birth'}),
            'taluka_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Taluka of Birth'}),
            'previous_school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous School'}),
            'previous_school_GR_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous School GR No'}),
            'date_of_school_leaving': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'last_class_studied': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Class in which Studying & Since When'}), ##Class in which Studying & Since When
            'reason_of_school_leaving': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reason of School Leaving'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'exam_year': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_month': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'progress': forms.TextInput(attrs={'class': 'form-control'}),
            'conduct': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks'}),
            'parent_cnic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent CNIC'}),
            'cell_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cell No'}),
            'nadra_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NADRA ID'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'placeholder': 'Upload Profile Image'}),  # Widget for image

        }
        
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If creating new instance, prefill with "Good"
        if not self.instance or not getattr(self.instance, 'pk', None):
            self.fields['progress'].initial = "Good"
            self.fields['conduct'].initial = "Good"
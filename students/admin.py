from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('GR_no', 'name', 'father_name', 'caste', 'date_of_birth', 'previous_school_GR_no', 'image')
    search_fields = ('GR_no', 'name', 'father_name', 'caste')
    list_filter = ('GR_no', 'name')

from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('personal_number', 'name', 'designation', 'bps', 'contact_number', 'cnic', 'staff_type')
    search_fields = ('personal_number', 'name', 'cnic', 'designation')
    list_filter = ('staff_type', 'designation')

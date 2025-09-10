from django.db import models

class Staff(models.Model):
    TEACHING = 'Teaching'
    NON_TEACHING = 'Non-Teaching'

    STAFF_TYPE_CHOICES = [
        (TEACHING, 'Teaching'),
        (NON_TEACHING, 'Non-Teaching'),
    ]

    personal_number = models.CharField(max_length=20, primary_key=True, verbose_name="Personal Number")
    name = models.CharField(max_length=100, verbose_name="Name")
    father_name = models.CharField(max_length=100, verbose_name="Father's Name")
    contact_number = models.CharField(max_length=15, verbose_name="Contact Number")
    designation = models.CharField(max_length=50, verbose_name="Designation")
    bps = models.IntegerField(verbose_name="BPS")  # Basic Pay Scale
    cnic = models.CharField(max_length=15, verbose_name="CNIC")
    account_no = models.CharField(max_length=30, verbose_name="Account Number")
    qualification = models.CharField(max_length=100, null=True, blank=True, verbose_name="Qualification")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    date_of_appointment = models.DateField(null=True, blank=True, verbose_name="Date of Appointment")
    date_of_school_joining = models.DateField(verbose_name="Date of School Joining")
    date_of_school_leaving = models.DateField(null=True, blank=True, verbose_name="Date of School Leaving")  # New Field
    image = models.ImageField(upload_to='staff/images/', null=True, blank=True, verbose_name="Profile Image")
    staff_type = models.CharField(
        max_length=20,
        choices=STAFF_TYPE_CHOICES,
        default=NON_TEACHING,
        verbose_name="Staff Type"
    )

    def __str__(self):
        return f"{self.personal_number} - {self.name}"

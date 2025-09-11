from django.db import models




class Student(models.Model):
    # Auto-incrementing ID field (implicit, no need to declare explicitly in Django)
    GR_no = models.CharField(max_length=20, primary_key=True, unique=True)  # GR_no as primary key
    seat_no = models.CharField(max_length=20, blank=True, null=True)  # sea_no as primary key
    date_of_admission = models.DateField()
    admission_class = models.CharField(max_length=50)
    current_class = models.CharField(max_length=50)
    section = models.CharField(max_length=50)

    # Student's Details
    medium = models.CharField(max_length=50, choices=[('Sindhi', 'Sindhi'), ('Urdu', 'Urdu'), ('English', 'English')], default='Sindhi')
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    religion = models.CharField(max_length=10, choices=[('Muslim', 'Muslim'), ('Non-Muslim', 'Non-Muslim')], default='Muslim')
    name = models.CharField(max_length=100)  # Name of Student
    father_name = models.CharField(max_length=100)
    caste = models.CharField(max_length=50, blank=True, null=True)  # Allow NULL values in DB
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    district_of_birth = models.CharField(max_length=100)
    taluka_of_birth = models.CharField(max_length=100, blank=True, null=True)
    previous_school = models.CharField(max_length=200)
    previous_school_GR_no = models.CharField(max_length=20, blank=True, null=True)

    date_of_school_leaving = models.DateField(blank=True, null=True)
    last_class_studied = models.CharField(max_length=500,blank=True, null=True)
    reason_of_school_leaving = models.CharField(max_length=200, blank=True, null=True)
    exam_type = models.CharField(max_length=50, choices=[('Annual', 'Annual'), ('Supplementary', 'Supplementary')],  default='Annual')
    student_type = models.CharField(max_length=50, choices=[('Regular', 'Regular'), ('Private', 'Private')],  default='Regular')
    exam_year = models.CharField(max_length=50, blank=True, null=True)
    exam_month = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    progress = models.CharField(max_length=100, default="Good", blank=True, null=True)
    conduct = models.CharField(max_length=100, default="Good", blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    # Parent/Guardian Information
    parent_cnic = models.CharField(max_length=15, blank=True, null=True)  # CNIC format validation can be added later
    cell_no = models.CharField(max_length=15, blank=True, null=True)  # Phone number
    nadra_id = models.CharField(max_length=20, blank=True, null=True)  # NADRA ID
    image = models.ImageField(upload_to='students/images/', null=True, blank=True, verbose_name="Profile Image")


    def __str__(self):
        return f"{self.GR_no} - {self.name}"

from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from weasyprint import HTML
from reportlab.lib.utils import ImageReader
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import date
from reportlab.pdfbase.pdfmetrics import stringWidth

import os
import datetime

# Dictionary for day numbers with ordinal words
ORDINALS = {
    1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
    6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth",
    11: "Eleventh", 12: "Twelfth", 13: "Thirteenth", 14: "Fourteenth",
    15: "Fifteenth", 16: "Sixteenth", 17: "Seventeenth", 18: "Eighteenth", 19: "Nineteenth",
    20: "Twentieth", 21: "Twenty First", 22: "Twenty Second", 23: "Twenty Third",
    24: "Twenty Fourth", 25: "Twenty Fifth", 26: "Twenty Sixth",
    27: "Twenty Seventh", 28: "Twenty Eighth", 29: "Twenty Ninth",
    30: "Thirtieth", 31: "Thirty First"
}

# Months
MONTHS = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

import inflect
p = inflect.engine()

def date_to_words(date_str):
    """
    Convert date in format DD-MM-YYYY to words like 'Sixth February Two Thousand Nine'
    """
    # Parse date
    date_obj = datetime.datetime.strptime(date_str, "%d-%m-%Y")
    
    day = date_obj.day
    month = date_obj.month
    year = date_obj.year

    # Convert
    day_word = ORDINALS[day]
    month_word = MONTHS[month]
    year_word = p.number_to_words(year, andword="")  # e.g., 2009 -> "two thousand nine"
    
    # Capitalize properly
    year_word = year_word.title()
    
    return f"{day_word} {month_word} {year_word}"


def bold(text):
    """Return a tuple marking this text as bold."""
    return (text, True)

def normal(text):
    """Return a tuple marking this text as normal."""
    return (text, False)

def draw_mixed_text(p, x, y, parts, size=14, font="Helvetica", bold_font="Helvetica-Bold"):
    """
    Draws text with bold and normal parts.

    Parameters:
    - p: ReportLab canvas object
    - x, y: Starting position
    - parts: List of (text, is_bold) tuples
    - size: Font size
    - font: Normal font
    - bold_font: Bold font
    """
    current_x = x
    for text, is_bold in parts:
        p.setFont(bold_font if is_bold else font, size)
        p.drawString(current_x, y, text)
        current_x += p.stringWidth(text, bold_font if is_bold else font, size)



# Helper function: Centered Image with optional horizontal shift
def draw_centered_image(p, path, y, width, height, x_offset=0):
    """
    Draws an image horizontally centered on the PDF page,
    with optional left/right offset.
    :param p: reportlab canvas
    :param path: image file path
    :param y: vertical position from bottom
    :param width: desired image width
    :param height: desired image height
    :param x_offset: +ve = move right, -ve = move left
    """
    if os.path.exists(path):
        try:
            image = ImageReader(path)
            page_width, _ = A4
            x_center = (page_width - width) / 2 + x_offset
            p.drawImage(image, x_center, y,
                        width=width, height=height,
                        preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print("Image drawing error:", e)


def draw_justified_text(p, x, y, text, width, size=14, font="Times-Italic", line_height=None):
    """
    Draws justified text on the PDF canvas with proper line wrapping and adjustable line spacing.

    Parameters:
    - p: ReportLab canvas object
    - x, y: Starting position
    - text: The text to be justified
    - width: The total width for justification
    - size: Font size (default: 14)
    - font: Font type (default: "Times-Italic")
    - line_height: Custom line spacing (default: font size + 2)
    """
    if line_height is None:
        line_height = size + 2  # Default extra spacing

    p.setFont(font, size)
    lines = text.split("\n")  # Support for manual line breaks

    for line in lines:
        words = line.split()
        if not words:
            y -= line_height  # Extra spacing for blank line
            continue

        current_line = []
        current_width = 0

        for word in words:
            word_width = p.stringWidth(word, font, size)
            if current_width + word_width <= width:
                current_line.append(word)
                current_width += word_width + p.stringWidth(" ", font, size)
            else:
                # Draw the current line (justified)
                _draw_justified_line(p, x, y, current_line, width, size, font, last_line=False)
                y -= line_height  # 👈 custom spacing
                current_line = [word]
                current_width = word_width + p.stringWidth(" ", font, size)

        # Draw the last line (left aligned, no justification)
        if current_line:
            _draw_justified_line(p, x, y, current_line, width, size, font, last_line=True)
            y -= line_height  # 👈 custom spacing

def _draw_justified_line(p, x, y, words, width, size, font, last_line=False):
    """
    Helper function to draw a single justified line of text.
    """
    if not words:
        return

    if last_line or len(words) == 1:
        # Left-align last line (no justification)
        current_x = x
        for word in words:
            p.drawString(current_x, y, word)
            current_x += p.stringWidth(word, font, size) + p.stringWidth(" ", font, size)
    else:
        # Justify the line
        text_width = sum(p.stringWidth(word, font, size) for word in words)
        space_width = (width - text_width) / (len(words) - 1)
        current_x = x
        for word in words:
            p.drawString(current_x, y, word)
            current_x += p.stringWidth(word, font, size) + space_width


def draw_underlined_text(p, x, y, text, size=14, font="Courier-Bold", center=False):
    """
    Draws underlined text on the PDF canvas.
    If center=True, text is horizontally centered on A4 page.
    """
    p.setFont(font, size)
    text_width = p.stringWidth(text, font, size)

    if center:
        page_width, _ = A4
        x = (page_width - text_width) / 2

    p.drawString(x, y, text)
    p.line(x, y - 2, x + text_width, y - 2)

@login_required
# def download_character_certificate(request, GR_no):
#     student = Student.objects.get(GR_no=GR_no)
#     html_content = render_to_string('certificate.html', {'student': student})
#     pdf = HTML(string=html_content).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{student.GR_no}_certificate.pdf"'
#     return response



@login_required
def download_character_certificate(request, GR_no):
    student = Student.objects.get(GR_no=GR_no)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.GR_no}_character_certificate.pdf"'
    
    p = canvas.Canvas(response)
    page_width, page_height = A4

    draw_underlined_text(p, 0, page_height - 50, "GOVERNMENT HIGH SCHOOL THARI(CAMPUS)", size=22, font="Times-Bold", center=True)

    logo_path = os.path.join(settings.BASE_DIR, 'students', 'static', 'students', 'images', 'logo.png')

    # Certificate Title
    draw_underlined_text(p, 0, page_height - 170, "CHARACTER CERTIFICATE", size=20, font="Helvetica-Bold", center=True)
    
    # G.R No (left-aligned, just below)
    draw_underlined_text(p, 60, page_height - 200, f"G.R No: {student.GR_no}", size=12, font="Helvetica-Bold", center=False)
   
  
    # Logo
    draw_centered_image(p, logo_path, y=page_height - 180, width=150, height=150)

 

    dob_formatted = student.date_of_birth.strftime("%d-%m-%Y")


    # Example of body text (uncomment when needed)
    certificate_text = (
    f"This is to certify that Mr./Mrs. {student.name} "
    f" son/daughter of {student.father_name}, caste {student.caste},"
    f" is a bonafide student of this school. \n He/She bears good moral character and his/her general conduct was good. \n"
    f" According to the school record his/her date of birth is {dob_formatted}.")
     
  # Draw justified text
    draw_justified_text(
        p,
        100, 600,                 # x, y position
        certificate_text,         # variable used here 
        width=400,
        size=14,
        font="Times-Italic",
        line_height=22

    )
    

   # Current Date (below certified statement)
    today = date.today().strftime("%d-%m-%Y")
    y = -140  # distance from top

    p.setFont("Times-Italic", 12)
    p.drawString(60, page_height-400, f"Date of Issue {today}")
    p.showPage()
    p.save()
    
    return response




# Create Student
@login_required
def create_student(request):
    if request.method == 'POST':
        #print(f"request.FILES: {request.FILES}")  # Debugging file upload
        form = StudentForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/create_student.html', {'form': form})

# Read (List Students)
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})



# Update Student
@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        print(f"request.FILES: {request.FILES}")  # Debugging file upload
        form = StudentForm(request.POST, request.FILES, instance=student)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/update_student.html', {'form': form})

# Delete Student
@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/delete_student.html', {'student': student})

def debug_student(request, GR_no):
    student = Student.objects.get(GR_no=GR_no)
    return JsonResponse(model_to_dict(student))


from reportlab.lib.pagesizes import A4

def draw_signature_section(p, text_left, text_center, text_right):
    page_width, page_height = A4
    y = 80  # distance from bottom

    # Text positions (left, center, right)
    left_x = 140
    center_x = page_width / 2
    right_x = page_width - 140

    font_size = 10
    p.setFont("Times-Roman", font_size)

    # --- Left ---
    # text_left = "Signature of Incharge G.R"
    p.drawCentredString(left_x, y, text_left)
    # Overline
    text_width = p.stringWidth(text_left, "Helvetica", font_size)
    p.line(left_x - text_width/2, y + 10, left_x + text_width/2, y + 10)

    # --- Center ---
    # text_center = "Signature of Class Teacher"
    p.drawCentredString(center_x, y, text_center)
    text_width = p.stringWidth(text_center, "Helvetica", font_size)
    p.line(center_x - text_width/2, y + 10, center_x + text_width/2, y + 10)

    # --- Right ---
    # text_right = "Signature of Head Master"
    p.drawCentredString(right_x, y, text_right)
    text_width = p.stringWidth(text_right, "Helvetica", font_size)
    p.line(right_x - text_width/2, y + 10, right_x + text_width/2, y + 10)




def draw_watermark(p, image_path, page_width, page_height, opacity=0.1, size=400):
    """
    Draws a watermark image in the center of the PDF page.

    Parameters:
    - p: ReportLab canvas object
    - image_path: Path to the watermark image
    - page_width, page_height: Dimensions of the page
    - opacity: Transparency of the watermark (0.0 to 1.0)
    - size: Width of watermark image (height will scale automatically)
    """
    if os.path.exists(image_path):
        from reportlab.pdfgen import canvas
        # Save current state
        p.saveState()

        # Set transparency
        p.setFillAlpha(opacity)

        # Calculate x, y for center position
        x = (page_width - size) / 2
        y = (page_height - size) / 2

        # Draw image
        watermark = ImageReader(image_path)
        p.drawImage(watermark, x, y, width=size, height=size, preserveAspectRatio=True, mask='auto')

        # Restore state (important, so following text/images are normal)
        p.restoreState()


@login_required
def download_leaving_certificate(request, GR_no):

    student = Student.objects.get(GR_no=GR_no)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.GR_no}_leaving_certificate.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4
    # Header
    # Draw border rectangle
   # Outer rectangle
    p.setLineWidth(2)
    p.rect(20, 30, page_width - 40, page_height - 40)

    # Inner rectangle
    p.setLineWidth(1)
    p.rect(30, 40, page_width - 60, page_height - 60)


    #######################

    draw_underlined_text(p, 0, page_height - 50, "GOVERNMENT HIGH SCHOOL THARI(CAMPUS)", size=22, font="Times-Bold", center=True)

    logo_path = os.path.join(settings.BASE_DIR, 'students', 'static', 'students', 'images', 'logo.png')
    
    draw_watermark(p, logo_path, page_width, page_height, opacity=0.1, size=900)

    if student.image and student.image.name:
        profile_image_path = student.image.path
    else:
        profile_image_path = os.path.join(settings.BASE_DIR, 'students', 'static', 'students', 'images', 'default-image.png')


    # Certificate Title
    draw_underlined_text(p, 0, page_height - 170, "SCHOOL LEAVING CERTIFICATE", size=20, font="Helvetica-Bold", center=True)
    
    # G.R No (left-aligned, just below)
    draw_underlined_text(p, 60, page_height - 200, f"G.R No: {student.GR_no}", size=12, font="Helvetica-Bold", center=False)
    
    # Logo
    draw_centered_image(p, logo_path, y=page_height - 180, width=150, height=150)

    #profile image
    draw_centered_image(p, profile_image_path, y=page_height - 290, width=100, height=100, x_offset=200)

    # Print ALL student fields instead of certificate text
    data = model_to_dict(student)
    dob_formatted = student.date_of_birth.strftime("%d-%m-%Y")
    doadmission_formatted = student.date_of_admission.strftime("%d-%m-%Y")
        
    if student.date_of_school_leaving:
        date_of_school_leaving_formatted = student.date_of_school_leaving.strftime("%d-%m-%Y")
    else:
        date_of_school_leaving_formatted = ""        

    date_in_figures =  date_to_words(dob_formatted)
    
    fields_to_print = [
        ("Name of Student", student.name.upper()),
        ("Father's Name", student.father_name.upper()),
        ("Religion", student.religion.upper()),
        ("Caste/Surname", student.caste.upper()),
        ("Place of Birth", student.place_of_birth),
        ("Date of Birth", dob_formatted),
        ("Date of Birth (in words)", date_in_figures),
        ("Last School Attended", student.previous_school),
        ("Date of Admission", doadmission_formatted),
        ("Class in which Admitted", student.admission_class),
        ("Class in which Studying & Since When", student.last_class_studied),
        ("Reason of Leaving School", student.reason_of_school_leaving),
        ("Date of Leaving School", date_of_school_leaving_formatted),
        ("Progress", student.progress),
        ("Conduct",  student.conduct),
        ("Remarks", student.remarks),
       
    ]
  
    # Print fields8
    p.setFont("Times-Roman", 12)
    y = page_height - 250  # starting position under logo

    for i, (label, value) in enumerate(fields_to_print, start=1):
        # Draw label in normal font
        p.setFont("Times-Italic", 12)
        p.drawString(60, y, f"{i:02d}. {label}: ")

        # Draw value in bold font
        p.setFont("Times-BoldItalic", 12)
        p.drawString(280, y, str(value))  # aligned a bit to the right

        y -= 20


    # Certified Statement (no number, smaller font, extra spacing before)
    y -= 20
    p.setFont("Times-BoldItalic", 10)
    p.drawString(60, y, "Certified that the above information is in accordance with the General Register of this institute.")

 
    
    # Current Date (below certified statement)
    today = date.today().strftime("%d-%m-%Y")
    y -= 20
    p.setFont("Times-Roman", 12)
    p.drawString(60, y, f"Date of Issue {today}")
    
    text_left = "Signature of Incharge G.R"
    text_center = "Signature of Class Teacher"
    text_right = "Signature of Head Master"

    draw_signature_section(p, text_left, text_center, text_right)

    p.showPage()
    p.save()
    return response    
    




@login_required
def download_tesimonial_certificate(request, GR_no):

    student = Student.objects.get(GR_no=GR_no)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.GR_no}_testimonial_certificate.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    page_width, page_height = A4
    # Header
    # Draw border rectangle
    # Outer rectangle
    p.setLineWidth(2)
    p.rect(20, 30, page_width - 40, page_height - 40)

    # Inner rectangle
    p.setLineWidth(1)
    p.rect(30, 40, page_width - 60, page_height - 60)

    draw_underlined_text(p, 0, page_height - 50, "GOVERNMENT HIGH SCHOOL THARI(CAMPUS)", size=22, font="Times-Bold", center=True)

    logo_path = os.path.join(settings.BASE_DIR, 'students', 'static', 'students', 'images', 'logo.png')

    draw_watermark(p, logo_path, page_width, page_height, opacity=0.1, size=900)

    # Certificate Title
    draw_underlined_text(p, 0, page_height - 170, "TESTIMONIAL CERTIFICATE", size=20, font="Helvetica-Bold", center=True)
    
    # G.R No (left-aligned, just below)
    draw_underlined_text(p, 60, page_height - 200, f"G.R No: {student.GR_no}", size=12, font="Helvetica-Bold", center=False)
   
  
    # Logo
    draw_centered_image(p, logo_path, y=page_height - 180, width=150, height=150)

    # Print ALL student fields instead of certificate text
    # data = model_to_dict(student)
    dob_formatted = student.date_of_birth.strftime("%d-%m-%Y")
        
    if student.date_of_school_leaving:
        date_of_school_leaving_formatted = student.date_of_school_leaving.strftime("%d-%m-%Y")
    else:
        date_of_school_leaving_formatted = ""        

    date_in_words =  date_to_words(dob_formatted)
    
    # Print fields8
    y = page_height - 250  # starting position under logo
    p.setFont("Times-Italic", 12)
    part = " II "    
    if student.current_class == "9":
        part = " I "
    
    today = date.today()
    current_year = today.year
    last_year = current_year - 1
    # session = f"{last_year} - {current_year}"  
     
    certificate_text = (
    f"       This is to certify that Mr./Mrs. {student.name.upper()}"
    f" S/O {student.father_name.upper()}, Surname {student.caste.upper()},"
    f" Has appeared in the Secondary School Certificate Part II {student.exam_type}"
    f" Examination {student.exam_year} under seat no {student.seat_no} Group {student.section}"
    f" from this School {student.student_type} student conducted by the Board of Intermediate and"
    f" Secondary Education Hyderabad in the month of {student.exam_month} and  was"
    f" placed Successful With Grade '{student.grade}'\n \n"
    f" His/Her date of birth according to General Register is {dob_formatted} \n"
    f" in words {date_in_words} \n \n"
    f" He/She bears a good moral character")
    
    draw_justified_text(
        p,
        100, y,                 # x, y position
        certificate_text,         # variable used here
        width=400,
        size=14,
        font="Times-Italic",
        line_height=22
    )
    # Current Date (below certified statement)
    today = date.today().strftime("%d-%m-%Y")
    y -= 280
    p.setFont("Times-Italic", 12)
    p.drawString(60, y, f"Date of Issue {today}")
    
   
    text_left = "Signature of Incharge G.R"
    text_center = "Signature of First Assistant"
    text_right = "Signature of Head Master"

    draw_signature_section(p, text_left, text_center, text_right)

    p.showPage()
    p.save()
    return response    
    

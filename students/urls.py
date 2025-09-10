from django.urls import path
from . import views

urlpatterns = [
    
        
    path('students/', views.student_list, name='student_list'),
    path('create/', views.create_student, name='create_student'),
    path('update/<int:pk>/', views.update_student, name='update_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('download-character-certificate/<str:GR_no>/', views.download_character_certificate, name='download_character_certificate'),
    path('download_leaving_certificate/<str:GR_no>/', views.download_leaving_certificate, name='download_leaving_certificate'),
    path('download_tesimonial_certificate/<str:GR_no>/', views.download_tesimonial_certificate, name='download_tesimonial_certificate'),

]
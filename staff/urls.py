from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_list, name='staff_list'),  # Staff list view
    path('add/', views.add_staff, name='add_staff'),  # Add staff view
    path('update/<int:pk>/', views.update_staff, name='update_staff'),  # Update staff view
    path('delete/<int:pk>/', views.delete_staff, name='delete_staff'),  # Delete staff view
]

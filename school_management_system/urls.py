from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from staff import views as staff_views  # Import staff views for 'register'
from django.views.generic import RedirectView  # For homepage redirection
from . import views  # Import project-level views for dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect homepage to login page
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),

    # Auth-related paths
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', staff_views.register, name='register'),  # Assuming `register` is in staff views
    # Dashboard path
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),  # Add this line for profile

    # Include app-specific URLs
    path('students/', include('students.urls')),
    path('staff/', include('staff.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

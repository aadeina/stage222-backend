# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth & user management
    path('api/auth/', include('accounts.urls')), 
    # Domain-specific modules
    path('api/candidates/', include('candidates.urls')),  
    path('api/recruiters/', include('recruiters.urls')),   
    path('api/organizations/', include('organizations.urls')),
    path('api/internships/', include('internships.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/messages/', include('messaging.urls')),
    path('api/bookmarks/', include('bookmarks.urls')),


]

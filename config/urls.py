from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth endpoints
    path('api/auth/', include('accounts.urls')),

    # Modular app URLs (future-proofed)
    path('api/candidates/', include('candidates.urls')),
    path('api/recruiters/', include('recruiters.urls')),
    path('api/organizations/', include('organizations.urls')),
    path('api/internships/', include('internships.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/messaging/', include('messaging.urls')),
    path('api/skills/', include('skills.urls')),
]

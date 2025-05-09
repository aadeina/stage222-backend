from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse  # <-- Add this
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Stage222 API",
      default_version='v1',
      description="Interactive documentation for the Stage222 internship platform",
      contact=openapi.Contact(email="amarmed4500@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# ✅ This is your health check view
def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('', health_check),  # ✅ Add this route

    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')), 
    path('api/candidates/', include('candidates.urls')),  
    path('api/recruiters/', include('recruiters.urls')),   
    path('api/organizations/', include('organizations.urls')),
    path('api/internships/', include('internships.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/messages/', include('messaging.urls')),
    path('api/bookmarks/', include('bookmarks.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

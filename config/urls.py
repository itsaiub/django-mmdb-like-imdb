from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

# handler404 = '404.html'

MEDIA_FILE_PATHS = static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('', include('user.urls', namespace='user')),
] + MEDIA_FILE_PATHS

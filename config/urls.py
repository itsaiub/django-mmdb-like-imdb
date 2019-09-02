from django.contrib import admin
from django.urls import path, include

# handler404 = '404.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
]

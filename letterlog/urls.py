from django.contrib import admin
from django.conf    import settings
from django.urls    import path, include

urlpatterns = [
    path('postboxes', include('postboxes.urls', namespace='postboxes'))
]

if settings.ADMIN_ENABLED:
    urlpatterns += [path('admin/', admin.site.urls)]

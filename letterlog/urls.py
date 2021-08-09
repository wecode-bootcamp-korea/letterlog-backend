from django.urls import path, include

urlpatterns = [
    path('postboxes', include('postboxes.urls'))
]

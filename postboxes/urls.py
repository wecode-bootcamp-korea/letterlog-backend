from django.urls    import path

from postboxes.views    import PostboxListAPIView

app_name = 'postboxes'

urlpatterns = [
    path('', PostboxListAPIView.as_view()),
]

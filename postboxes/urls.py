from django.urls    import path

from postboxes.views    import PostboxAccessAPIView

urlpatterns = [
    path('/access', PostboxAccessAPIView.as_view())
]

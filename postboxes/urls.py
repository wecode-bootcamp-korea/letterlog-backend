from django.urls    import path

from postboxes.views    import LetterListAPIView

urlpatterns = [
    path('/collection', LetterListAPIView.as_view())
]

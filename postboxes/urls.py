from django.urls    import path

from postboxes.views    import PostboxView, AccessView
urlpatterns = [
    path(''             , PostboxView.as_view()),
    path('/<postbox_id>', AccessView.as_view())
]
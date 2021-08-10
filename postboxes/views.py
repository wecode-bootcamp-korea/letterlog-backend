from django.db.models   import Q

from rest_framework.generics   import ListCreateAPIView
from rest_framework.filters    import SearchFilter, OrderingFilter

from postboxes.models      import Postbox
from postboxes.serializers import PostboxSerializer

class PostboxListAPIView(ListCreateAPIView):
    serializer_class = PostboxSerializer
    filter_backends  = [OrderingFilter]
    ordering_fields  = ['send_at', 'closed_at', 'days_to_close', 'created_at']
    ordering         = ['-created_at']

    def get_queryset(self, *args, **kwargs):
        status        = self.request.GET.get('status')
        search        = self.request.GET.get('search', '')
        search_option = self.request.GET.get('search_option')

        q = Q(days_to_close__gte=0)

        status_set = {
            'public'  : Q(is_public=True),
            'private' : Q(is_public=False)
        }

        search_set = {
            'exact' : Q(name=search),
            'naive' : Q(name__icontains=search)
        }

        q &= status_set.get(status, Q()) & search_set.get(search_option, Q())

        return Postbox.objects.filter(q)

from django.db.models   import Q

from rest_framework.generics   import ListCreateAPIView
from rest_framework.filters    import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from postboxes.models      import Postbox
from postboxes.serializers import PostboxListSerializer

class PostboxListAPIView(ListCreateAPIView):
    serializer_class = PostboxListSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields   = ['name']
    ordering_fields = ['send_at', 'closed_at', 'days_to_close', 'created_at']
    ordering        = ['-created_at']

    def get_queryset(self, *args, **kwargs):
        status = self.request.GET.get('status') 

        q = Q(days_to_close__gte=0)

        if status == 'public':
            q &= Q(is_public=True)
        elif status == 'private':
            q &= Q(is_public=False)

        return Postbox.objects.filter(q) 

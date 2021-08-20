from django.db.models   import Q

from rest_framework.generics import ListAPIView

from postboxes.serializers  import LetterListSerializer
from postboxes.models import Letter

class LetterListAPIView(ListAPIView):
    serializer_class = LetterListSerializer

    pagination_class = None
    ordering = ['-created_at']

    def get_queryset(self):
        uuid = self.request.GET.get('uuid')

        q = Q(postbox__uuid=uuid)

        return Letter.objects.filter(q)

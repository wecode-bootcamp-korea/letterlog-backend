from django.db.models   import Q

from rest_framework          import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.filters  import SearchFilter, OrderingFilter
from rest_framework.views    import APIView
from rest_framework.response import Response

from postboxes.models      import Postbox, Letter
from postboxes.serializers import (
    PostboxListCreateSerializer,
    PostboxAccessSerializer,
    LetterCreateSerializer,
    LetterListSerializer,
    CollectionAccessSerializer
)
from postboxes.authentication import PostboxAuthentication, CollectionAuthentication

class PostboxListCreateAPIView(ListCreateAPIView):
    serializer_class = PostboxListCreateSerializer

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

class PostboxAccessAPIView(APIView):
    def post(self, request):
        serializer = PostboxAccessSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendLetterAPIView(CreateAPIView):
    authentication_classes = [PostboxAuthentication, ]

    serializer_class = LetterCreateSerializer


class CollectionAPIView(ListAPIView):
    authentication_classes = [CollectionAuthentication, ]

    serializer_class = LetterListSerializer

    ordering = ['-created_at']

    def get_queryset(self):
        uuid = self.request.GET.get('uuid')

        q = Q(postbox__uuid=uuid)

        return Letter.objects.filter(q)

class CollectionAccessAPIView(APIView):
    def post(self, request):
        serializer = CollectionAccessSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

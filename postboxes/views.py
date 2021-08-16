from rest_framework          import status
from rest_framework.views    import APIView
from rest_framework.response import Response

from postboxes.serializers  import PostboxAccessSerializer

class PostboxAccessAPIView(APIView):
    def post(self, request):
        serializer = PostboxAccessSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

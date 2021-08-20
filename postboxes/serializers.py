from rest_framework.serializers import ModelSerializer

from postboxes.models   import Letter

class LetterListSerializer(ModelSerializer):
    class Meta:
        model = Letter
        fields = ['nickname', 'image_url', 'caption']

from django.contrib.auth.hashers    import check_password

from rest_framework             import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions  import AuthenticationFailed, ValidationError

from postboxes.models   import Postbox

class PostboxAccessSerializer(ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Postbox
        fields = ['id', 'password', 'token']
        read_only_fields = ['token']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def validate(self, data):
        postbox = Postbox.objects.filter(id=data.get('id')).first()

        if postbox is None:
            raise ValidationError("Postbox Not Found")

        if not check_password(data.get('password'), postbox.password):
            raise AuthenticationFailed("Wrong Password")

        data['token'] = postbox.token

        return data

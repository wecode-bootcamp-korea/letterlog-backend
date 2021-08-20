import re

from datetime   import timedelta

from django.contrib.auth.hashers             import make_password, check_password
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.utils                            import timezone
from django.db                               import transaction

from rest_framework.serializers import ModelSerializer, IntegerField, UUIDField, ImageField
from rest_framework.exceptions  import AuthenticationFailed, ValidationError

from postboxes.models import Postbox, Receiver, Letter
from postboxes.utils  import AWSAPI

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class ReceiverSerializer(ModelSerializer):
    class Meta:
        model  = Receiver
        fields = ['email']

    def validate_email(self, value):
        if not re.match(EMAIL_REGEX, value):
            raise ValidationError("Wrong Email")

class PostboxListCreateSerializer(ModelSerializer):
    receivers = ReceiverSerializer(many=True, write_only=True)

    class Meta:
        model  = Postbox 
        fields = ['id', 'name', 'is_public', 'password', 'send_at', 'closed_at', 'days_to_close', 'receivers']
        read_only_fields = ['id', 'closed_at', 'days_to_close']
        extra_kwargs = {
            'password'  : {'write_only': True, 'allow_blank':True},
        }

    def validate(self, data):
        if not data.get('is_public'):
            MinimumLengthValidator(8).validate((data.get('password')))

        if Postbox.objects.filter(days_to_close__gte=0, name=data.get('name')).exists():
            raise ValidationError("This is a duplicated name")

        self.closed_at     = data.get('send_at') - timedelta(days=1)
        self.days_to_close = (self.closed_at - timezone.localtime().date()).days

        if self.days_to_close < 6:
            raise ValidationError("Send Date should be after 7days from today")

        if not data.get('receivers'):
            raise ValidationError("There should be at least one receiver")

        return data

    def create(self, validated_data):
        receivers_data = self.initial_data.get('receivers')
        receivers_data = [dict(t) for t in {tuple(receiver.items()) for receiver in receivers_data}]

        with transaction.atomic():
            postbox = Postbox.objects.create(
                uuid          = Postbox.get_available_uuid(),
                name          = validated_data['name'],
                is_public     = validated_data['is_public'],
                password      = make_password(validated_data['password']) if not validated_data['is_public'] else None,
                send_at       = validated_data['send_at'],
                closed_at     = self.closed_at,
                days_to_close = self.days_to_close
            )
            for receiver_data in receivers_data:
                Receiver.objects.create(postbox=postbox, **receiver_data)

        return postbox

class PostboxAccessSerializer(ModelSerializer):
    id = IntegerField(write_only=True)

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

        if postbox.is_public:
            raise ValidationError("Postbox is Public")

        if not check_password(data.get('password'), postbox.password):
            raise AuthenticationFailed("Wrong Password")

        data['token'] = postbox.token

        return data

class LetterCreateSerializer(ModelSerializer):
    image = ImageField(write_only=True)

    class Meta:
        model = Letter
        fields = ['nickname', 'caption', 'image']

    def validate(self, data):
        self.postbox = self.context['request'].user

        if not self.postbox:
            raise ValidationError("No Postbox")

        return data

    def create(self, validated_data):
        aws = AWSAPI()

        letter = Letter.objects.create(
            nickname  = validated_data['nickname'],
            image_url = aws.upload_file(validated_data['image']),
            caption   = validated_data['caption'],
            postbox   = self.postbox
        )

        return letter

class CollectionAccessSerializer(ModelSerializer):
    uuid = UUIDField(write_only=True)

    class Meta:
        model = Postbox
        fields = ['uuid', 'password', 'token']
        read_only_fields = ['token']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def validate(self, data):
        postbox = Postbox.objects.filter(uuid=data.get('uuid')).first()

        if postbox is None:
            raise ValidationError("Collection Not Found")

        if postbox.is_public:
            raise ValidationError("Collection is Public")

        if not check_password(data.get('password'), postbox.password):
            raise AuthenticationFailed("Wrong Password")

        data['token'] = postbox.token

        return data

class LetterListSerializer(ModelSerializer):
    class Meta:
        model = Letter
        fields = ['nickname', 'image_url', 'caption']

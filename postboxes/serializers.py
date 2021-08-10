import re
import bcrypt
from datetime   import timedelta

from django.contrib.auth.hashers             import make_password
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.dispatch.dispatcher              import receiver
from django.utils                            import timezone
from django.db                               import transaction

from rest_framework.serializers import ModelSerializer, ValidationError

from postboxes.models import Postbox, Receiver

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class ReceiverSerializer(ModelSerializer):
    class Meta:
        model  = Receiver
        fields = ['email']

    def validate_email(self, value):
        if not re.match(EMAIL_REGEX, value):
            raise ValidationError("Wrong Email")
        return value

class PostboxSerializer(ModelSerializer):
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
        receivers_data = validated_data.get('receivers')
        deduplicated_receivers_data = [dict(t) for t in {tuple(receiver.items()) for receiver in receivers_data}]
        
        with transaction.atomic():
            postbox = Postbox.objects.create(
                uuid          = Postbox.get_available_uuid(),
                name          = validated_data['name'],
                is_public     = validated_data['is_public'],
                password      = make_password(validated_data['password'], bcrypt.gensalt()) if not validated_data['is_public'] else None,
                send_at       = validated_data['send_at'],
                closed_at     = self.closed_at,
                days_to_close = self.days_to_close
            )
            Receiver.objects.bulk_create([
                Receiver(
                    postbox = postbox,
                    email   = receiver_data['email']
                ) for receiver_data in deduplicated_receivers_data]
            )

        return postbox

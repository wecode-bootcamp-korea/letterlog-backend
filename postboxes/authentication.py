import jwt

from django.conf    import settings
from django.utils   import timezone

from rest_framework import authentication, exceptions

from postboxes.models   import Postbox

class PostboxAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        postbox_id = request.parser_context['kwargs']['postbox_id']
        access_token = request.headers.get('Authorization')

        postbox = Postbox.objects.filter(id=postbox_id).first()

        if postbox is None:
            raise exceptions.NotFound('Postbox Not Found')

        if postbox.days_to_close < 0:
            raise exceptions.NotAcceptable('Postbox is Inactive')

        if not postbox.is_public:
            if not access_token:
                raise exceptions.AuthenticationFailed('Need Token')

            try: 
                payload = jwt.decode(access_token, settings.SECRET_KEY, settings.SECRET_ALGORITHM)
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('access_token expired')

            if postbox.id != payload.get('postbox_id'):
                raise exceptions.AuthenticationFailed('Invalid Token')

        return (postbox, None)

class CollectionAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        uuid = request.query_params['uuid']
        access_token = request.headers.get('Authorization')

        postbox = Postbox.objects.filter(uuid=uuid).first()

        if postbox is None:
            raise exceptions.NotFound('Postbox Not Found')

        if postbox.send_at < timezone.localtime().date():
            raise exceptions.NotAcceptable("It's Not time yet")

        if not postbox.is_public:
            if not access_token:
                raise exceptions.AuthenticationFailed('Need Token')

            try: 
                payload = jwt.decode(access_token, settings.SECRET_KEY, settings.SECRET_ALGORITHM)
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('access_token expired')
            except jwt.DecodeError:
                raise exceptions.AuthenticationFailed('Invalid Token')

            if postbox.id != payload.get('postbox_id'):
                raise exceptions.AuthenticationFailed('Invalid Token')

        return (postbox, None)


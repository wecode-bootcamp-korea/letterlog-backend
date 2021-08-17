import jwt

from django.conf    import settings

from rest_framework import authentication, exceptions

from postboxes.models   import Postbox

class PostboxAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.headers.get('Authorization')

        if not access_token:
            return None
        try:
           payload = jwt.decode(access_token, settings.SECRET_KEY, settings.SECRET_ALGORITHM)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        
        postbox = Postbox.objects.filter(id=payload['postbox_id']).first()

        if postbox is None:
            raise exceptions.AuthenticationFailed('Postbox not found')

        if postbox.days_to_close < 0:
            raise exceptions.AuthenticationFailed('postbox is inactive')

        return (postbox, None)

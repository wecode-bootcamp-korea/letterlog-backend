import jwt

from django.http    import JsonResponse

from postboxes.models   import Postbox
from django.conf        import settings

def access_validator(function):
    def wrapper(self, request, postbox_id, *args, **kwargs):
        try:
            postbox = Postbox.objects.get(id=postbox_id)

            if not postbox.is_open:
                return JsonResponse({"message": "EXPIRED_POSTBOX"}, status=406)

            if not postbox.is_public:
                access_token = request.headers.get('Authorization')

                if not access_token:
                    return JsonResponse({"message": "NEED_PASSWORD"}, status=401)

                payload = jwt.decode(access_token, settings.SECRET_KEY, settings.SECRET_ALGORITHM)

                if payload['postbox_id'] != postbox.id:
                    return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

            request.postbox = postbox

            return function(self, request, postbox_id, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

        except Postbox.DoesNotExist:
            return JsonResponse({"message": "INVALID_POSTBOX"}, status=400)

    return wrapper

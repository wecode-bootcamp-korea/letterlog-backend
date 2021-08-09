import json
import bcrypt, jwt
from datetime import datetime

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q
from django.db          import transaction

from postboxes.models   import Postbox, Receiver
from django.conf        import settings

class PostboxView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data['name']

            if Postbox.objects.filter(is_open=True, name=name).exists():
                return JsonResponse({"message": "DUPLICATE_NAME"}, status=406)

            emails = set(data['emails'])

            if not emails:
                return JsonResponse({"message": "EMPTY_EMAIL"}, status=406)

            open_at   = datetime.strptime(data['openAt'], '%Y-%m-%d').date()
            closed_at = datetime.strptime(data['closedAt'], '%Y-%m-%d').date()

            if not Postbox.validate_date(open_at=open_at, closed_at=closed_at):
                return JsonResponse({"message": "INVALID_DATE"}, status=406)

            password  = data.get('password')
            is_public = not bool(password)

            if not is_public:
                if not Postbox.validate_password(password):
                    return JsonResponse({"message": "INVALID_PASSWORD"}, status=406)

                hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()

            with transaction.atomic():
                postbox = Postbox.objects.create(
                    uuid      = Postbox.get_available_uuid(),
                    name      = name,
                    password  = hashed_password if not is_public else None,
                    is_public = is_public,
                    open_at   = open_at,
                    closed_at = closed_at
                )

                Receiver.objects.bulk_create([
                    Receiver(
                        postbox = postbox,
                        email   = email
                    ) for email in emails
                ])

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

    def get(self, request):
        status = request.GET.get('status')
        search = request.GET.get('search')

        q = Q(is_open=True)

        if status:
            if status == 'public':
                q &= Q(is_public=True)
            elif status == 'private':
                q &= Q(is_public=False)
            else:
                return JsonResponse({"message": "INVALID_STATUS"}, status=406)

        if search:
            q &= Q(name__contains=search)

        postboxes = Postbox.objects.filter(q).order_by('-created_at')

        results = {
            'postboxes':[
                {
                    'id'       : postbox.id,
                    'name'     : postbox.name,
                    'isPublic' : postbox.is_public,
                    'openAt'   : postbox.open_at,
                    'closedAt' : postbox.closed_at
                } for postbox in postboxes
            ]
        }

        return JsonResponse({"results": results}, status=200)

class AccessView(View):
    def post(self, request, postbox_id):
        try:
            data = json.loads(request.body)

            postbox = Postbox.objects.get(id=postbox_id)

            if not postbox.is_open:
                return JsonResponse({"message": "EXPIRED_POSTBOX"}, status=406)

            if postbox.is_public:
                return JsonResponse({"message": "PUBLIC_POSTBOX"}, status=406)

            if not bcrypt.checkpw(data['password'].encode('UTF-8'), postbox.password.encode('UTF-8')):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({'postbox_id': postbox.id}, settings.SECRET_KEY, settings.SECRET_ALGORITHM)

            return JsonResponse({"accessToken": access_token}, status=200)

        except Postbox.DoesNotExist:
            return JsonResponse({"message": "INVALID_ID"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "JSON_ERROR"}, status=400)

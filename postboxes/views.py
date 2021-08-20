from django.views           import View
from django.http            import JsonResponse
from django.core.paginator  import Paginator, InvalidPage

from postboxes.models       import Postbox, Letter

class CollectionView(View):
    def get(self, request, postbox_uuid):
        try:
            postbox = Postbox.objects.filter(uuid=postbox_uuid).first()

            if postbox is None:
                return JsonResponse({'message':'Invalid_uuid'}, status=400)

            postboxes   = Letter.objects.filter(postbox=postbox)

            paginator   = Paginator(postboxes, 40)

            page_number = request.GET.get('page')

            results     = paginator.page(int(page_number))

            result = [{
                'id'        : postbox.id,
                'nickname'  : postbox.nickname,
                'image_url' : postbox.image_url,
                'caption'   : postbox.caption
            }for postbox in results.object_list]

            return JsonResponse({'message':'SUCCESS', 'result':result}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except InvalidPage:
            return JsonResponse({'message':'INVALID_PAGE'},status=400)
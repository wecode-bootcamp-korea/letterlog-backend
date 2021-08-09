from django.db.models	import Q
from django.utils		import timezone

from postboxes.models	import Postbox

def update_postbox_open_status():
	today = timezone.localtime().date()

	q  = Q(is_open=True)
	q &= Q(closed_at__lt=today)

	Postbox.objects.filter(q).update(is_open=False)

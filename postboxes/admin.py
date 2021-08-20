from django.contrib import admin

from .models    import Postbox, Letter, Receiver

admin.site.register(Postbox)
admin.site.register(Letter)
admin.site.register(Receiver)

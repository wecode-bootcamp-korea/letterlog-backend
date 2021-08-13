import uuid
import jwt
from datetime   import datetime, timedelta

from django.conf    import settings
from django.db      import models

class Postbox(models.Model):
    id            = models.BigIntegerField(primary_key=True)
    uuid          = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name          = models.CharField(max_length=100)
    password      = models.CharField(max_length=200, null=True)
    is_public     = models.BooleanField(default=True)
    send_at       = models.DateField()
    closed_at     = models.DateField()
    days_to_close = models.IntegerField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'postboxes'

    @property
    def token(self):
        payload = {
            'postbox_id' : self.id,
            'exp'        : datetime.utcnow() + timedelta(minutes=60),
            'iat'        : datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, settings.SECRET_ALGORITHM)

        return token

class Letter(models.Model):
    postbox    = models.ForeignKey('Postbox', on_delete=models.CASCADE)
    nickname   = models.CharField(max_length=100)
    image_url  = models.CharField(max_length=2000)
    caption    = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'letters'

class Receiver(models.Model):
    postbox    = models.ForeignKey('Postbox', on_delete=models.CASCADE)
    email      = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table    = 'receivers'
        constraints = [
            models.UniqueConstraint(fields=['postbox', 'email'], name='unique_postbox_email')
        ]

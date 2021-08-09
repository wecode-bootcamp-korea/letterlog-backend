import uuid
from datetime import timedelta

from django.db      import models
from django.utils   import timezone

DELTA_DAY = 7

class Postbox(models.Model):
    uuid       = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name       = models.CharField(max_length=100)
    password   = models.CharField(max_length=200, null=True)
    is_public  = models.BooleanField(default=True)
    open_at    = models.DateField()
    closed_at  = models.DateField()
    is_open    = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'postboxes'

    @classmethod
    def check_uuid_exists(cls, _uuid):
        manager = getattr(cls, '_default_manager')
        return manager.filter(uuid=_uuid).exists()

    @classmethod
    def get_available_uuid(cls):
        row_uuid = uuid.uuid4()
        while cls.check_uuid_exists(_uuid=row_uuid):
            row_uuid = uuid.uuid4()
        return row_uuid

    @staticmethod
    def validate_password(password):
        return isinstance(password, str) and len(password) >= 8

    @staticmethod
    def validate_date(open_at, closed_at):
        if open_at - closed_at < timedelta(days=DELTA_DAY):
            return False

        if closed_at < timezone.localtime().date():
            return False

        return True

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

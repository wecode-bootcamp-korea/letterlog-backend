import uuid

from django.db      import models

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

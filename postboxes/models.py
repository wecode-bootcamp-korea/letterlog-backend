import uuid

from django.db.models.base           import Model
from django.db.models.deletion       import CASCADE
from django.db.models.fields         import BooleanField, CharField, DateField, DateTimeField, UUIDField
from django.db.models.fields.related import ForeignKey

class Postbox(Model):
    unique_id   = UUIDField(default=uuid.uuid4, editable=False)
    name        = CharField(max_length=50)
    password    = CharField(max_length=200, null=True)
    is_public   = BooleanField(default=False)
    open_at     = DateField()
    closed_at   = DateField()
    is_open     = BooleanField(default=False)
    created_at  = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'postboxes'

class receivers(Model):
    email       = CharField(max_length=200)
    created_at  = DateTimeField(auto_now_add=True)
    postbox     = ForeignKey('Postbox', on_delete=CASCADE)

    class Meta:
        db_table = 'receivers'

class Letter(Model):
    nickname    = CharField(max_length=100)
    image_url   = CharField(max_length=2000)
    caption     = CharField(max_length=100)
    created_at  = DateTimeField(auto_now_add=True)
    postbox     = ForeignKey('Postbox', on_delete=CASCADE)

    class Meta:
        db_table = 'letters'
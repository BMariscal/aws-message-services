import uuid
from django.db import models
from django.db.models.signals import post_save

from upload.signals import notify_user


class Emoji(models.Model):
    class Meta:
        db_table = 'emoji'
    indexes = [
        models.Index(fields=['uuid', ]),
        models.Index(fields=['image_url', ]),
        models.Index(fields=['name', ]),

    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)
    uploaded_by = models.CharField(max_length=500)
    tags = models.TextField(max_length=500)



class Tag(models.Model):
    class Meta:
        db_table = 'tag'
    tag = models.CharField(max_length=30, unique=True)
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE)

post_save.connect(notify_user, sender=Emoji)

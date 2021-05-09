from itertools import chain

from django.db import models
from django.db.models.signals import post_save

from upload.signals import notify_user



class PrintableModel(models.Model):
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        return data

    class Meta:
        abstract = True


class Emoji(PrintableModel):
    class Meta:
        db_table = 'emoji'
    indexes = [
        models.Index(fields=['uuid', ]),
        models.Index(fields=['image_url', ]),
        models.Index(fields=['name', ]),

    ]
    name = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)
    uploaded_by = models.CharField(max_length=500)
    tags = models.TextField(max_length=500)



class Tag(PrintableModel):
    class Meta:
        db_table = 'tag'
    tag = models.CharField(max_length=30, unique=False)
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE)

post_save.connect(notify_user, sender=Emoji)

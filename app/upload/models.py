from django.db import models
from django.db.models.signals import post_save

from upload.signals import notify_user


class Emojis(models.Model):
    name = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)


class Tags(models.Model):
    tag = models.CharField(max_length=30, unique=True)


class EmojiTag(models.Model):
    emoji = models.ForeignKey(Emojis, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)


post_save.connect(notify_user, sender=Emojis)

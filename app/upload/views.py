import logging
from django.db.utils import IntegrityError
from django.db import transaction

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from upload.models import Emojis, EmojiTag, Tags

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def valid_input(request) -> bool:
    """
    Input Good?
    :param request: request object
    :return: Bool
    """
    image_file = request.FILES["image_file"]
    if not image_file:
        return False
    name = request.POST.get("name")
    if not name:
        return False
    return True


@transaction.atomic
def image_upload(request):
    if request.method == "POST" and "image_file" in request.FILES:
        if not valid_input(request):
            return render(request, "upload.html")

        tag = request.POST.get("tag")  # optional
        image_file = request.FILES["image_file"]
        name = request.POST.get("name")

        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)  # TODO: s3 this bitch
        image_url = fs.url(filename)

        emoji = Emojis(image_url=image_url, name=name)
        emoji.save()
        if tag:
            try:
                with transaction.atomic():
                    tag = Tags(tag=tag)
                    tag.save()
            except IntegrityError as e:
                logger.warning("Error", e)
                emoji_tag = EmojiTag(emoji=emoji, tag=tag)
                emoji_tag.save()

        return render(request, "upload.html", {
            "image_url": image_url
        })
    return render(request, "upload.html")

import logging

from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from upload.models import Emojis, EmojiTag, Tags
from upload.helpers.upload_image import upload_emoji_image

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


@csrf_exempt
def image_upload(request):
    if request.method == "POST" and "image_file" in request.FILES:
        if not valid_input(request):
            return render(request, "upload.html")

        tag = request.POST.get("tag")  # optional
        image_file = request.FILES["image_file"]
        name = request.POST.get("name")

        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        s3_link = upload_emoji_image(image_file, image_file.name)

        emoji = Emojis(image_url=image_url, name=name)
        emoji.save()
        if tag:
            try:
                tag_exists = Tags.objects.filter(tag=tag).exists()
                if not tag_exists:
                    with transaction.atomic():
                        tag = Tags(tag=tag)
                        tag.save()
            except IntegrityError as e:
                logger.warning("Error", e)
                emoji_tag = EmojiTag(emoji=emoji, tag=tag)
                emoji_tag.save()
        return render(request, "upload.html", {
            "image_url": s3_link
        })

    return render(request, "upload.html")

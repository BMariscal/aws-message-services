import logging

from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from upload.helpers.fetch_images import retrieve_emoji_images
from upload.helpers.upload_image import upload_emoji_image
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


@csrf_exempt
@ratelimit(key='ip', rate='10/h')
def image_upload(request):
    if request.method != "POST":
        return render(request, "upload.html")

    if request.method == "POST" and "image_file" in request.FILES:
        if not valid_input(request):
            return render(request, "upload.html")

        tag = request.POST.get("tag", "generic")  # optional
        image_file = request.FILES["image_file"]
        name = request.POST.get("name", "anon")
        s3_link = upload_emoji_image(image_file, image_file.name)

        emoji = Emojis(image_url=s3_link, name=name)
        emoji.save()
        tag_used = None
        try:
            tag_used = Tags.objects.filter(tag=tag).first()
            if not tag_used:
                with transaction.atomic():
                    tag_used = Tags(tag=tag)
                    tag_used.save()
        except IntegrityError as e:
            logger.warning("Error", e)
        emoji_tag = EmojiTag(emoji=emoji, tag=tag_used)
        emoji_tag.save()
        return render(request, "upload.html", {
            "image_url": s3_link
        })

    return render(request, "upload.html")

@csrf_exempt
def get_images(request):
    if request.method != "GET":
        return HttpResponse("Invalid method.")

    emojis = retrieve_emoji_images()
    return render(request, "emojis.html", {
        "emojis": emojis
    })

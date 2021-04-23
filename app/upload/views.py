import logging
from typing import List

from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from upload.helpers.fetch_images import retrieve_emoji_images
from upload.helpers.upload_image import upload_emoji_image
from upload.models import Emoji, Tag

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

def create_tags(emoji: Emoji, tags_list: List):
    """
    Bulk create tags for a given emoji.
    :param emoji:  Emoji object
    :param tags_list: list of tag names
    """
    if not tags_list:
        return

    tags = []
    for tag in tags_list:
        tag_record = Tag(emoji=emoji, tag=tag)
        tags.append(tag_record)

    Tag.objects.bulk_create(tags)



@csrf_exempt
@ratelimit(key='ip', rate='10/h')
def image_upload(request):
    if request.method != "POST":
        return render(request, "upload.html")

    if request.method == "POST" and "image_file" in request.FILES:
        if not valid_input(request):
            return render(request, "upload.html")

        tags_string = request.POST.get("tags", "generic")  # optional
        tags_list = tags_string.split(",")

        image_file = request.FILES["image_file"]
        name = request.POST.get("name", "anon")
        uploaded_by = request.POST.get("author", "anonymous")

        s3_link = upload_emoji_image(image_file, image_file.name)

        try:
            emoji = Emoji(image_url=s3_link, name=name, uploaded_by=uploaded_by, tags=tags_list)
            emoji.save()
            create_tags(emoji, tags_list)
        except IntegrityError as e:
            logger.warning("Error", e)
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

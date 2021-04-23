from upload.models import Emoji


def retrieve_emoji_images():
    emojis_with_tags = Emoji.objects.values_list("name", "image_url", "uploaded_by", "tags")
    return emojis_with_tags

from upload.models import Emojis, EmojiTag, Tags



def retrieve_emoji_images():
    emojis = Emojis.objects.values_list("name", "image_url")
    return emojis

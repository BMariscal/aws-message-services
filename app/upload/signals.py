
from upload.utils import publish_event


def notify_user(sender, instance, **kwargs):
    publish_event(instance)

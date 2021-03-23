import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def publish_event(instance):
    logger.info(f"<<PUBLISHING EVENT>>: {instance.name}")

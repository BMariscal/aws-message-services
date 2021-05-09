import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .message_service.message_handler import (
    publish_message_to_queue,
    publish_message_to_event_bridge,
    read_from_sqs_queue
)

def publish_event(instance) -> bool:
    try:
        instance_dict = instance.to_dict()
        #publish_message_to_queue(instance_dict)
        publish_message_to_event_bridge(instance_dict)
    except Exception as e:
        logger.error(f"Failed to publish event for {instance.name}. Error: {e}")
        return False

    logger.info(f"<<PUBLISHED EVENT>>: {instance.name}")
    return True



def read_events():
    messages = read_from_sqs_queue()
    for message in messages:
        print("MESSAGE:", message)
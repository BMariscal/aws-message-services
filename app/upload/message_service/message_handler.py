"""
Event Bridge:
1. publish_message_to_event_bridge
2. AWS EventBridge publishes message to second queue
3. read_from_sqs_queue reads EventBridge events from second queue

SQS:
1. publish_message_to_queue enqueues event to first queue
2. Lambda function polls from first queue, does something to data, sends it to second queue

"""
import json
import logging
import os

import boto3

REGION_NAME = os.environ.get("REGION_NAME")
FIRST_QUEUE_URL = os.environ.get("FIRST_SQS_QUEUE_URL")
SECOND_QUEUE_URL = os.environ.get("SECOND_QUEUE_URL")
RESOURCE_ARN = os.environ.get("RESOURCE_ARN")
SOURCE = os.environ.get("SOURCE")

kwargs = {
          "region_name": os.environ.get("REGION_NAME"),
          "aws_access_key_id":os.environ.get("AWS_KEY"),
          "aws_secret_access_key":os.environ.get("AWS_SECRET")
          }

event_bridge_client = boto3.client('events', **kwargs)

logger = logging.getLogger(__name__)

def publish_message_to_queue(payload: dict):
    kwargs["endpoint_url"] = FIRST_QUEUE_URL
    sqs_client = boto3.client("sqs", **kwargs)
    try:
        logger.info(f"Sending immediate event to {FIRST_QUEUE_URL}")
        sqs_client.send_message(
            QueueUrl=FIRST_QUEUE_URL,
            MessageBody=json.dumps(payload)
        )
    except Exception as e:
        logger.exception(f"Error queuing event: {str(e)}")
        return


def publish_message_to_event_bridge(payload: dict):
    try:
        logger.info(f"Sending immediate event to EventBridge")
        response = event_bridge_client.put_events(
            Entries=[
                {
                    'Detail': json.dumps(payload),
                    'DetailType': "emojiSubmitted",
                    'Resources': [
                        RESOURCE_ARN,
                    ],
                    'Source': SOURCE
                }
            ]
        )
    except Exception as e:
        logger.exception(f"Error sending event to EventBridge: {str(e)}")
        return

    logger.info("EventBridge Entries:", response['Entries'])
    read_from_sqs_queue()

def read_from_sqs_queue():
    kwargs["endpoint_url"] = SECOND_QUEUE_URL
    sqs_client = boto3.client("sqs", **kwargs)
    queue_url = os.environ.get("SECOND_QUEUE_URL")

    data = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
    )
    messages = data.get("Messages", [])
    all_event_data = []
    for message in messages:
        body_dict = json.loads(message["Body"])
        event_data = body_dict.get("detail")
        logger.info("Data Retrieved from EventBridge:", event_data)
        all_event_data.append(event_data)

    return all_event_data

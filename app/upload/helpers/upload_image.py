import io
import mimetypes
import os

import boto3
from PIL import Image

client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get("AWS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET"),
)

MAX_SIZE = (128, 128)
BUCKET = os.environ.get("S3_BUCKET")
REGION_NAME = os.environ.get("REGION_NAME")
URL = f"https://{BUCKET}.s3.{REGION_NAME}.amazonaws.com/"


def upload_emoji_image(image, image_name):
    file_name = str(image_name)
    img = Image.open(image)

    out_img = io.BytesIO()
    try:
        img.thumbnail(MAX_SIZE)
        img.save(out_img, img.format)
        out_img.seek(0)
        mime_type = mimetypes.guess_type(image_name)[0]
        # Upload image to s3
        client.upload_fileobj(out_img, BUCKET, file_name, ExtraArgs={"ACL": "public-read", "ContentType": mime_type})
    except Exception as e:
        print("Exception raised: ", e)
        return False

    return URL + file_name

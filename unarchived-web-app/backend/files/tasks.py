import os
from google.cloud import vision
from google.cloud.vision_v1 import types
from .models import UploadedFile
from django.conf import settings
from celery import shared_task
import tempfile

@shared_task
def run_ocr_on_file(file_id):
    try:
        uploaded = UploadedFile.objects.get(id=file_id)
        uploaded.status = 'processing'
        uploaded.save()

        client = vision.ImageAnnotatorClient()

        # Download file to temp path
        file_path = uploaded.file.path
        with open(file_path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)
        response = client.document_text_detection(image=image)

        if response.error.message:
            uploaded.status = 'failed'
            uploaded.parsed_output = {'error': response.error.message}
        else:
            uploaded.status = 'done'
            uploaded.parsed_output = {
                'text': response.full_text_annotation.text,
                'pages': [p.text for p in response.full_text_annotation.pages]
            }

        uploaded.save()
    except Exception as e:
        if uploaded:
            uploaded.status = 'failed'
            uploaded.parsed_output = {'error': str(e)}
            uploaded.save()
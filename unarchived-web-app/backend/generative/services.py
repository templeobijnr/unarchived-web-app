# generative/services.py

import replicate
import logging
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.conf import settings

# Setup logging
logger = logging.getLogger(__name__)

class ImageGenerationService:
    def __init__(self):
        """Initialize the service with clients for Replicate and AWS S3."""
        self.replicate_client = None
        self.s3_client = None
        
        # Initialize Replicate client
        try:
           self.replicate_client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
           logger.info("Replicate client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Replicate client: {e}")
        
        # Initialize AWS S3 client (boto3)
        try:
            self.s3_client = boto3.client(
                's3', 
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            logger.info("AWS S3 client initialized successfully.")
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"Failed to initialize AWS S3 client: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize AWS S3 client: {e}")

    def generate_image(self, model_id, inputs):
        """Generate an image using Replicate API."""
        try:
            logger.info(f"Generating image using model {model_id}.")
            model = self.replicate_client.models.get(model_id)
            prediction = model.predict(**inputs)
            logger.info("Image generation successful.")
           # return prediction
        except Exception as e:
            logger.error(f"Error during image generation: {e}")
            return None
    
    def upload_to_s3(self, image_data, bucket_name, file_name):
        """Upload the generated image to AWS S3."""
        try:
            response = self.s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=image_data,
                ContentType="image/jpeg"
            )
            logger.info(f"Image uploaded successfully to {bucket_name}/{file_name}.")
            return response
        except Exception as e:
            logger.error(f"Error uploading image to S3: {e}")
            return None

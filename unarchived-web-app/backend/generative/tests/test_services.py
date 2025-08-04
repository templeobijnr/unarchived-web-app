from django.test import TestCase
from generative.services import ImageGenerationService
from unittest.mock import patch

class ImageGenerationServiceTest(TestCase):

    def setUp(self):
        self.image_service = ImageGenerationService()

    def test_generate_image(self):
        inputs = {
            'input_image': 'sample_input_image',
            'model_id': 'stable-diffusion',  # Example model
        }
        result = self.image_service.generate_image(model_id='stable-diffusion', inputs=inputs)
        self.assertIsNotNone(result)
        self.assertIn('image_url', result)  # Assuming your Replicate API returns an image URL

    @patch('generative.services.boto3.client')
    def test_upload_to_s3(self, mock_boto_client):
        mock_s3 = mock_boto_client.return_value
        mock_s3.put_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        image_service = ImageGenerationService()
        image_data = b"fake_image_data"
        bucket_name = 'test-bucket'
        file_name = 'test_image.jpeg'

        result = image_service.upload_to_s3(image_data, bucket_name, file_name)
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)
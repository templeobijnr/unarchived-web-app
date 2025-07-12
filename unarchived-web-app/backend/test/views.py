from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from google.cloud import vision
from google.cloud.vision_v1 import types
import tempfile

class TestVisionOCRView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name

            client = vision.ImageAnnotatorClient()
            with open(temp_path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)
            response = client.document_text_detection(image=image)

            if response.error.message:
                return Response({"error": response.error.message}, status=500)

            return Response({
                "text": response.full_text_annotation.text
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
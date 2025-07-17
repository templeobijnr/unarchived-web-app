from rest_framework import serializers
from .models import UploadedFile

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'original_filename', 'file_type', 'size', 'created_at', 'status']

    def create(self, validated_data):
        uploaded_file = validated_data.get('file')
        validated_data['original_filename'] = uploaded_file.name
        validated_data['file_type'] = uploaded_file.content_type
        validated_data['size'] = uploaded_file.size
        return super().create(validated_data)
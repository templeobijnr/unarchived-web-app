from rest_framework import serializers
from .models import DigitalProductGenome

class DigitalProductGenomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProductGenome
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')
from rest_framework import serializers
from .models import DigitalProductGenome

class DigitalProductGenomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProductGenome
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')
    
    def to_representation(self, instance):
        """Add custom handling for serialized data."""
        representation = super().to_representation(instance)
        if "data" in representation:
            # Process dynamic fields (like materials, components) if necessary
            pass  # Add any custom logic here to process complex data structures
        return representation
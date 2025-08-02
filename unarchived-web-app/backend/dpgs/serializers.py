# dpgs/serializers.py
from rest_framework import serializers
from .models import DigitalProductGenome, DPGComponent, ComponentSpecification, ApparelDPGExtension, GeneratedAsset

class DPGComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DPGComponent
        fields = ['id', 'name', 'description', 'order']

class ComponentSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentSpecification
        fields = ['id', 'component', 'material', 'color', 'size', 'quantity', 'notes']

class ApparelDPGExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApparelDPGExtension
        fields = ['id', 'fabric_composition', 'sizing_chart', 'fit_information', 'construction_details', 'hardware_components', 'colorways', 'cost_breakdown', 'manufacturing_data']

class GeneratedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedAsset
        fields = ['id', 'file', 'description', 'created_at']

class DigitalProductGenomeSerializer(serializers.ModelSerializer):
    components = DPGComponentSerializer(many=True, read_only=True)
    apparel_extension = ApparelDPGExtensionSerializer(read_only=True)
    assets = GeneratedAssetSerializer(many=True, read_only=True)

    class Meta:
        model = DigitalProductGenome
<<<<<<< HEAD
        fields = ['id', 'title', 'description', 'version', 'data', 'stage', 'created_at', 'updated_at', 'components', 'apparel_extension', 'assets']
        read_only_fields = ['id', 'owner','created_at', 'updated_at']
=======
        fields = '__all__'
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')
    
    def to_representation(self, instance):
        """Add custom handling for serialized data."""
        representation = super().to_representation(instance)
        if "data" in representation:
            # Process dynamic fields (like materials, components) if necessary
            pass  # Add any custom logic here to process complex data structures
        return representation
>>>>>>> 7053c7ac760f8b7cc6e95ccb374ef373c20c11b9

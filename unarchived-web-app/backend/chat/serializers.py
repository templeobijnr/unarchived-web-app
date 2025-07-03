
class MessageSerializer(serializers.ModelSerializer):
    """Chat message serializer"""
    
    author_display = serializers.CharField(
        source='get_author_display', 
        read_only=True
    )
    
    class Meta:
        model = Message
        fields = [
            'id', 'author', 'author_display', 'content', 'timestamp', 'typing'
        ]
        read_only_fields = ['timestamp']


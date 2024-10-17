from rest_framework import serializers
from shortener.models.url_db import ShortenedURL, generate_unique_shortcode


class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = '__all__'
        read_only_fields = ['short_code', 'owner', 'secret_key']

    def create(self, validated_data):
        # Generate a random short code
        validated_data['short_code'] = generate_unique_shortcode()
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    

class PublicShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        exclude = ['secret_key', 'owner']
        read_only_fields = ['short_code', 'owner', 'secret_key']
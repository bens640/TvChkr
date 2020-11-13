from rest_framework import serializers
from .models import Show

class EmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
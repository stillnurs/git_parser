from rest_framework import serializers

from .models import Commits


class ScrapedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commits
        fields = '__all__'  # importing all fields

from rest_framework import serializers

from .models import *


class ScrapedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repository
        fields = ('url',)

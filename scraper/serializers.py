import asyncio
from rest_framework import serializers
from .ascrape import scraper


class ScrapedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = asyncio.run(scraper())
        fields = ('commits',)

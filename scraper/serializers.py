import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from rest_framework import serializers
from .ascrape import scraper


class ScrapedDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = asyncio.run(scraper())
        fields = ('commits',)

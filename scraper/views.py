import asyncio

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import ScrapedDataSerializer

from .ascrape import Scraper


class CommitsView(APIView):
    """Вывод данных репозитория"""

    def get(self, request, *args, **kwargs):
        queryset = Commits.objects.all()
        serializer = ScrapedDataSerializer(queryset, many=True)
        return Response(serializer.data)


class GetCommits:

    def commits_scraper(self):
        results = Scraper()
        return results

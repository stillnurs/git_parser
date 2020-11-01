from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import ScrapedDataSerializer


class RepositoryView(APIView):
    """Вывод данных репозитория"""

    def get(self, request):
        url = Repository.objects.all()
        serializer = ScrapedDataSerializer(url, many=True)
        return Response(serializer.data)

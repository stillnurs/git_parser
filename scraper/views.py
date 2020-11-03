

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import ScrapedDataSerializer


class CommitsView(APIView):
    """Вывод данных репозитория"""
    def __int__(self):
        self.queryset = Commits.objects.all()
        self.serializer = ScrapedDataSerializer(self.queryset, many=True)

    def get(self, request):
        return Response(self.serializer.data)




from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import News


class Counter(APIView):
    def get(self, request, pk):
        news = News.objects.get(id=pk)
        number_of_comments = news.comment_set.count()
        return Response({'number_of_comments': number_of_comments})

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from utils.pagination import LargeResultsSetPagination
from ...serializers import ArtistSerializer
from ...models import Artist

__all__ = (
    'ArtistListCreateView',
    'ArtistListUpdateDestroy',
)


#
# class ArtistListview(APIView):
#     def get(self, request):
#         artists = Artist.objects.all()
#         serializer = ArtistSerializer(artists, many=True)
#         return Response(serializer.data)


# Generic의 요소를 사용해서
# ArtistListCreateView,
# ArtistListUpdateDestroy View,
# 2개구현,
# url 연결
# postman api테스트
# 다실행해보기
# pagination

class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        print('request User:', request.user)
        return super().get(request, *args, **kwargs)


class ArtistListUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

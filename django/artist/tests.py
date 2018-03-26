import random

import math
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from artist.apis import ArtistListCreateView
from artist.serializers import ArtistSerializer
from .models import Artist


class ArtistListTest(APITestCase):
    VIEW_NAME = 'apis:artist:artist-list'
    PATH = '/api/artist/'
    VIEW = ArtistListCreateView
    MODEL = Artist
    PAGINATION_COUNT = 5

    def test_reverse(self):
        f"""
        Artist List에 해당하는 VIEW_NAME을 reverse한 결과가 기대 PATH와 같은지 검사
            VIEW_NAME :{self.VIEW_NAME}
            PATH : {self.PATH}
        :return:
        """

        reverse_url_name = reverse(self.VIEW_NAME)
        # print(reverse_url_name)

        self.assertEqual(reverse_url_name, self.PATH)

    def test_resolve(self):
        f"""
        Artist List에 해당하는 PATH를 resolve한 결과의 func와 view_name이
        기대하는 View.as_view()와 VIEW_NAME과 같은지 검사
            VIEW: {self.VIEW}
            PATH: {self.PATH}
            VIEW_NAME: {self.VIEW_NAME}
        :return:
        """

        resolver_match = resolve(self.PATH)

        self.assertEqual(
            resolver_match.func.__name__,
            self.VIEW.as_view().__name__,
        )
        self.assertEqual(
            resolver_match.view_name,
            self.VIEW_NAME,
        )

    def test_artist_list_count(self):
        # self.client에 get 요청
        # response.data를 사용
        # artist-list 요청 시알 수 있는 Artist개수가 기대값과 같은지 테스트
        # (테스트용 artist를 여러개 생성해야함)
        # artist = Artist.objects.all()
        num = random.randrange(1, 10)
        for i in range(num):
            Artist.objects.create(name=f'Artist{i}')

        response = self.client.get(self.PATH)
        self.assertEqual(
            response.data['count'],
            self.MODEL.objects.count(),
        )
        self.assertEqual(
            response.data['count'],
            num,
        )

        # self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # self.assertEqual(response.data.)

    def test_artist_list_pagination(self):
        num = 13
        for i in range(13):
            Artist.objects.create(name=f'Artist{i+1}')

        response = self.client.get(self.PATH, {'page': 1})
        # 응답코드 200 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # for를 사용해서 ,pagination된 모둔 page들에 요청 후 results값ㅇ르 확인하도록 구성
        ceil_num = math.ceil(num / self.PAGINATION_COUNT)
        print(ceil_num)
        for i in range(ceil_num):
            # 'results' 키에 5개의 데이터가 배열로 전달되는지 확인
            self.assertEqual(
                len(response.data['results']),
                self.PAGINATION_COUNT,
            )
            # 'results'키에 들어있는 5개의 Artist가 serialize되어있는 결과가
            # 실제 Queryset을 serialize한 결과가 같은지 확인
            self.assertEqual(
                response.data['results'],
                ArtistSerializer(Artist.objects.all()[:5], many=True).data,
            )

            print(f'iteration {i+1}')

        #
        # self.assertNotEqual(response.data['next'], 'NULL')

        # ArtistListCreateView.cls.pagination_class.page_size
        # r = ArtistListCreateView.as_view()
        # artist-list를


class ArtistCreateTest(APITestCase):
    def test_create_artist(self):
        # pass
        # /static/test/suji.jpg에 있는 파일을 이용해서
        # 나머지 데이터를 채워서 Artist객체를 생성
        # 이진데이터 모드로 연 '파일 객체'를
        # 생성할 Artist의 '파일 필드 명'으로 전달
        # self.client.post(URL, {'img.profile
    pass

from collections import namedtuple
from typing import NamedTuple

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from album.models import Album
from .models import Song


# Create your views here.
def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs,
    }
    # 전체 Artist목록을 ul>li로 출력
    # 템플릿은 'artist/list.html'을 사용
    # 전달할 context키는 'artist'를 사용

    return render(request, 'song/song_list.html', context)


def song_search(request):
    """
    1.사용할 URL : song/search
     사용할 TEMPLATE ; templates/song/song_search.html
        form안에 input 한개, button한개
        함수에서 return render
    2. get-post 분기
        1.input의 name을 keyword로 지정
        2.이 함수를 request.method가 'get일 떄와 'post'일 떄로 분기
        reuqest.method가 'post'일 떄
            request.post dict의 'keyword'키에 해당하는 값을
            httpresponse로 출력
        request.method가 'get'일 떄
            이전 템플릿 유지
    3. Query filter 로 검색하기
        keyword가 자신의 title에 포함되는 song쿼리셋 생성
        위 쿼리셋을 'songs'변수에 할당
        context dict를 만들고 "songs"키에 songs 변수를 할당
        render의 3번쨰 인수를 만들고 context로 전달
        template에 전달된 'songs'를 출력
            song_search.html을 그대로 사용
    :param request:
    :param title:
    :return:
    #
    # 0219 Homework
    # songs_from_artists
    # songs_from_albums
    # songs_from_title
    # 위 세변수에 위의조건 3개에 부합하는 쿼리셋을 각각 전달
    # 세 변수를 이용해 검색결과를 3단으로 분리해서 출력
    # -> 아티스트로 검색한 노래결과, 앨범으로 검색한 노래결과, 제목으로 검색한 노래결과
    """  # Song과 연결된 Artist의 name에 keyword가 포함되는 경우
    # Song과 연결된 Album의 name에 keyword가 포함되는 경우
    # 를 모두 포함하는 쿼리셋
    # print(request.GET)
    # print(type(request.GET))
    # print(request.GET.get('keyword'))

    # keyword에 빈값이 올 경우 QuerySet을 할당하지 않도록 수정
    # keyword = request.GET.keys()
    # keyword = request.GET['keyword']
    # song목록중 title이 keyword를 포함하는 쿼리셋

    context = {
        'song_infos': [],
    }
    keyword = request.GET.get('keyword')

    # SongInfo = namedtuple('SongInfo', ['type', 'q'])

    class SongInfo(NamedTuple):
        type: str
        q: Q

    if keyword:
        song_infos = (
            SongInfo(
                type='아티스트명',
                q=Q(album__artists__name__contains=keyword)),
            SongInfo(
                type='앨범명',
                q=Q(album__title__contains=keyword)),
            SongInfo(
                type='노래제목',
                q=Q(title__contains=keyword)),
        )

        for type, q in song_infos:
            context['song_infos'].append({
                'type': type,
                'songs': Song.objects.filter(q),
            })
    return render(request, 'song/song_search.html', context)

# else를 없애고 render 를 한번만 사용해서 get/post 요청을 모두처리
# return render(request, 'song/song_search.html')

# songs = Song.objects.filter(
#     Q(album__artists__name__contains=keyword) |
#     Q(title__contains=keyword)|
#     Q(album__title__contains=keyword)
# ).distinct

# filter 뒤의 조건을 Q Objects로 만들어서 for문에서 사용
# songs_from_title = Song.objects.filter(title__contains=keyword)
# songs_from_albums = Song.objects.filter(album__title__contains=keyword)
# songs_from_artists = Song.objects.filter(album__artists__name__contains=keyword)

# 미리선언한 context의 'songs'키에 Queryset을 할당

# context['songs_from_title'] = songs_from_title
# context['songs_from_albums'] = songs_from_albums
# context['songs_from_artists'] = songs_from_artists

# zip
# 1
# for type, songs in zip(('아티스트명', '앨범명', '노래제목'),
#                        (songs_from_artists, songs_from_albums, songs_from_title)):
#     context['song_infos'].append({
#         'type': type,
#         'songs': songs,
#     })
# 2
# context['song_infos'].append({
#     'type': '아티스트명',
#     'songs': songs_from_artists
# })
# context['song_infos'].append({
#     'type': '앨범명',
#     'songs': songs_from_albums
# })
# context['song_infos'].append({
#     'type': '노래제목',
#     'songs': songs_from_title
# })

# get 이면 빈상태로 render실행

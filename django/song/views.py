from django.http import HttpResponse
from django.shortcuts import render
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
    """
    context={}
    if request.method == 'POST':
        #keyword에 빈값이 올 경우 QuerySet을 할당하지 않도록 수정
        keyword = request.POST['keyword'].strip()
        # song목록중 title이 keyword를 포함하는 쿼리셋
        if keyword:
            songs = Song.objects.filter(title__contains=keyword)
            # 미리선언한 context의 'songs'키에 Queryset을 할당
            context['songs']= songs
            # context = {
            #     'songs': songs,
            # }
    #get 이면 빈상태로 render실행
    return render(request, 'song/song_search.html', context)
    # else를 없애고 render 를 한번만 사용해서 get/post 요청을 모두처리

    # return render(request, 'song/song_search.html')

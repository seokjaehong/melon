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

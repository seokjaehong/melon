from django.shortcuts import render
from .models import Album


# Create your views here.
def album_list(request):
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    # 전체 Artist목록을 ul>li로 출력
    # 템플릿은 'artist/list.html'을 사용
    # 전달할 context키는 'artist'를 사용

    return render(request, 'album/album_list.html', context)

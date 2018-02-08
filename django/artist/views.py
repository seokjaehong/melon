from django.shortcuts import render
from .models import Artist


# Create your views here.
def artist_list(request):
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }
    # 전체 Artist목록을 ul>li로 출력
    # 템플릿은 'artist/list.html'을 사용
    # 전달할 context키는 'artist'를 사용

    return render(request, 'artist/artist_list.html', context)

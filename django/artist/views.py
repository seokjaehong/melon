from django.http import HttpResponse
from django.shortcuts import render, redirect
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


def artist_add(request):
    # HTML에 Artist클래스가 받을 수 있는 모든 input을 구현
    # img_profile 제외
    # methomd가 POST면 request.POST에서 해당 데이터 처리
    #   새  ARTIST객체를 만들고 artist_list로 이동
    # method가 get 이면 arttist_add.html을 표시

    # if request.method == "POST":
    #     name = request.POST["name"]
    #     real_name = request.POST["real_name"]
    #     # nationality = request.POST["nationality"]
    #     # birth_date = request.POST["birth_date"]
    #     # constellation = request.POST["constellation"]
    #     # blood_type = request.POST["blood_type"]
    #     # intro = request.POST["intro"]
    #
    #     if name:
    #         artist = Artist.objects.create(
    #             name=name,
    #             real_name=real_name,
    #             # natioanlity=nationality,
    #             # birth_date=birth_date,
    #             # constellation=constellation,
    #             # blood_type=blood_type,
    #             # intro=intro,
    #         )
    #         artist.save()
        if request.method == "POST":
            return HttpResponse(request.POST['name'])
        else :
            return render(request, 'artist/artist_add.html')

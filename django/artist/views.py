
from django.shortcuts import render, redirect

from .models import Artist
import requests
from bs4 import  BeautifulSoup


def artist_list(request):
    artists = Artist.objects.all()
    context = {
        'artists': artists,
    }
    return render(
        request,
        'artist/artist_list.html',
        context,
    )


def artist_add(request):
    # HTML에 Artist클래스가 받을 수 있는 모든 input을 구현
    #   img_profile은 제외
    # method가 POST면 request.POST에서 해당 데이터 처리
    #   새 Artist객체를 만들고 artist_list로 이동
    # method가 GET이면 artist_add.html을 표시

    # ** 생년월일은 YYYY-MM-DD 형식으로 받음
    #      이후 datetime.strptime을 사용해서 date객체로 변환

    # 1. artist_add.html 작성
    # 2. url과 연결, /artist/add/ 에 매핑
    # 3. GET요청시 잘 되는지 확인
    # 4. form method설정 후 POST요청시를 artist_add() view에서 분기
    # 5. POST요청의 값이 request.POST에 잘 오는지 확인
    #       name값만 받아서 name만 갖는 Artist를 먼저 생성
    #       성공 시 나머지 값들을 하나씩 적용해보기
    # 6. request.POST에 담긴 값을 사용해 Artist인스턴스 생성
    # 7. 생성 완료 후 'artist:artist-list' URL name에 해당하는 view로 이동

    # 1. artist/artist_add.html에 Artist_add다 라는 내용만 표시
    #   url, view를 서로 연결
    #   artist/add/ URL사용

    # 2. aritst_add.html에 form을 하나 생성
    #       input은 name이 'name'인 요소 한개만 생성
    #       POST방식으로 전송 후, 전달받은 'name'값을 바로 HttpResponse로 보여주기

    # 3. 전송받은 name을 이용해서 Artist를 생성
    #       이후 'artist:artist-list'로 redirect

    if request.method == 'POST':
        name = request.POST['name']
        real_name = request.POST['real_name']
        nationality = request.POST['nationality']
        birth_date = request.POST['birth_date']
        constellation = request.POST['constellation']
        blood_type = request.POST['blood_type']
        intro = request.POST['intro']
        Artist.objects.create(
            name=name,
            real_name=real_name,
            nationality=nationality,
            birth_date=birth_date,
            constellation=constellation,
            blood_type=blood_type,
            intro=intro,
        )
        return redirect('artist:artist-list')
    else:
        return render(request, 'artist/artist_add.html')


def artist_search_from_melon(request):
    """
    template :artist /artist_search_from_melon.html
    form(input[name=keyword]한개, button한개
    1. form에 주어진' keyword'로 멜론 사이트의 아티스트 검색 결과를 크롤링
    2. 크롤링된  검색결과를 적절히 파싱해서 검색 결과 목록을 생성
        -> list내에 dict를 만드는 형태
        artist_info_list = [
        {'artist_id':261143, 'name':'아이유','url_img_cover':'http:...'},
        {'artist_id':261143, 'name':'아이유','url_img_cover':'http:...'},
        {'artist_id':261143, 'name':'아이유','url_img_cover':'http:...'},
        ]
    3. 해당 결과를 목록을 템플릿에 출력
        context = {'artist_info_list' : artist_info_list로 전달 후 템플릿에 사용
    :param request:
    :return:
    """

    keyword = request.GET.get('keyword')
    url = "https://www.melon.com/search/artist/index.htm"
    parameter = {
        'q': keyword,
        'section': '',
        'searchGnbYn': 'Y',
        'kkoSpl': 'N',
        'kkoDpType': '',
        'ipath': 'srch_form',
    }
    # response = requests.GET.get(url, parameter)
    # soup = BeautifulSoup(response.text, 'lxml')
    # # beutifulsoup을 통해 soup으로 퍼다담음
    # tr_list = soup.select('div#pageList div > ul > li')
    #
    # # 가수의 일반정보 :이름, 국적, 성별, 솔로/그룹 여부 , 장르 ,유명곡 정보를 한번에 받아오기 위해 li 까지만 내려받음
    # context = []
    # # 결과를 result에 내려받는 for 문
    # for tr in tr_list:
    #     # < a href = "javascript:searchLog('web_artist','ARTIST','AR','아이유','261143');melon.link.goArtistDetail('261143');"title = "아이유 - 페이지 이동"class ="ellipsis" > < b > 아이유 < / b > < / a >
    #
    #     artist_info = tr.find('div', class_='wrap_atist12').find('div', class_='atist_info')
    #     source = tr.find('div', class_='wrap_atist12').find('a', class_='thumb')
    #
    #     # print(source)
    #     # print(type(source))
    #     # source = artist_info.select_one('a:nth-of-type(1) href').get('value')
    #
    #     # r1 = re.compile(r'.*?\;.*?\'(\d.*)\'', re.DOTALL)
    #
    #     artist_id = re.search(r"searchLog\(.*'(\d+)'\)", source.get('href')).group(1)
    #     artistname = artist_info.find('a', class_='ellipsis').text
    #     artistname_gubun = artist_info.find('dd', class_='gubun').get_text(strip=True)
    #     artist_genre = artist_info.find('dd', class_='gnr').find('div', class_='fc_strong').get_text(strip=True)
    #
    #     artist = Artist(artist_id=artist_id, name=artistname, gubun=artistname_gubun, genre=artist_genre)
    #     context.append(artist)

    return render(request, 'artist/artist_search_from_melon.html')

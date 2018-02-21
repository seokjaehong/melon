from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ...models import Artist

__all__ = (
    'artist_add_from_melon',
)


def artist_add_from_melon(request):
    """
    POST요청을 받음
    request.POST artist_id

    artist_id를 사용해서
    멜론 사이트에서 Artist에 들어갈 상세정보를 가져옴

    name
    real_name
    nationality
    birth_date
    constellation
    blood_type
    intro

    1) 위데이터를 그대로 HttpResponse로 출력해보기

    를 채운 Artist를 생성, Db에 저장
    이후 artist:artist-list로 redirect

    :param request:
    :return:
    """
    if request.method == 'POST':
        url = f'https://www.melon.com/artist/detail.htm'
        artist_id = request.POST['artist_id']
        # url_img_cover = request.POST['url_img_cover']
        params = {
            'artistId': artist_id,
        }
        # print(type(request.POST))
        response = requests.get(url, params)
        source = response.text
        soup = BeautifulSoup(source, 'lxml')

        # div_entry = soup.find('div', class_='section_atistinfo04')
        div_detail_entry = soup.find('div', id='conts')
        # 이름
        artistname = soup.find('p', class_='title_atist').strong.next_sibling.strip()

        # info 정보
        if div_detail_entry.find('div', class_='section_atistinfo04') != None:
            personal_information_meta = div_detail_entry.find('div', class_='section_atistinfo04')
            dl4 = personal_information_meta.find('dl', class_='list_define clfix')
            items = [item.get_text(strip=True) for item in dl4.contents if not isinstance(item, str)]
            it = iter(items)
            personal_information = dict(zip(it, it))
        else:
            personal_information = ''

        real_name = personal_information.get('본명', '')
        nationality = personal_information.get('국적', '')
        birth_date = personal_information.get('생일', '')
        constellation = personal_information.get('별자리', '')
        blood_type = personal_information.get('혈액형', '')

        # blood_type과 birth_date_str 이 없는경우 걸러내기
        if birth_date == None:
            birth_date = ''

        if blood_type == None:
            blood_type = ''
        else:
            for short, full in Artist.CHOICES_BLOOD_TYPE:
                if blood_type.strip() == full:
                    blood_type = short
            else:
                blood_type = Artist.BLOOD_TYPE_OTHER

        # artist_id가 melon_id에 해당하는 Artist가 있다면
        # 해당 Artist의 내용을 update
        # 없으면 Artist를 생성

        artist, created = Artist.objects.update_or_create(
            melon_id=artist_id,
            name=artistname,
            real_name=real_name,
            nationality=nationality,
            birth_date=datetime.strptime(birth_date, '%Y.%m.%d'),
            constellation=constellation,
            blood_type=blood_type,
        )
        # print(created)
        # print(personal_information)
        return redirect('artist:artist-list')
        # return HttpResponse(personal_information.values)

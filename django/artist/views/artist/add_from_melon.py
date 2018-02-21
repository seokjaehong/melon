import re
from datetime import datetime
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from django.core.files import File
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

        # print(url_img_cover)
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

        # url_img_cover = request.POST['url_img_cover']
        url_img_cover_source = div_detail_entry.find('div',class_='wrap_thumb').find('img')#.find('src')
        r1 = re.compile(r'\;\".*\"(.*)\?', re.DOTALL)
        url_img_cover = re.search(r1, str(url_img_cover_source)).group(1)
        # print(url_img_cover)

        response = requests.get(url_img_cover)
        binary_data = response.content
        #ByteIO는 파일처럼 취급되는 객체인데, 메모리에서 데이터가 아무것도 없는 파일이 생성되었다고 가정한다.
        temp_file = BytesIO()
        #그리고 , 파일에 데이터를 쓴다.
        temp_file.write(binary_data)
        #다쓰고 이파일에 탐색시점을 처음으로 돌려놓는다. 이렇게 하면 템프파일은 파일이 기록된 객
        temp_file.seek(0)


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

        #프로필이 저장된 상태에서 url_image_cover를 업데이트한다.
        from pathlib import Path
        file_name = Path(url_img_cover).name
        #Path란 url_img_coverdp에서 파일이름만 꺼내오고 싶을때
        #즉 요런 파일 261143_500.jpg
        #정규식이 아니라 내장라이브라이브러리로 파일 이름만 뽑아낼 수 있음


        artist.img_profile.save(file_name,File(temp_file))
        #ByteIO를 저장할때는 File로 한번 더 감싸준다.
        #여기서 실제 File이 아니라 proxy역할을 해준다고 보면됨, 중개자 역할


        # artist.save()

        return redirect('artist:artist-list')
        # return HttpResponse(personal_information.values)





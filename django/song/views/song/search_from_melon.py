from django.shortcuts import render, redirect
import re
from ...models import Song
import requests
from bs4 import BeautifulSoup, NavigableString

__all__ = (
    'song_search_from_melon',
)


def song_search_from_melon(request):
    keyword = request.GET.get('keyword')
    # print(keyword)
    context = {}
    if keyword:
        import requests
        from bs4 import BeautifulSoup
        song_info_list = []
        url = 'https://www.melon.com/search/song/index.htm'
        params = {'q': keyword}
        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')
        # print(soup)

        tr_list = soup.select('form#frm_defaultList table > tbody > tr ')

        # tr_list = soup.find('form', id='frm_defaultList').find('table').find('tbody').find_all('tr')

        for tr in tr_list:
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            if tr.select_one('td:nth-of-type(3) a.fc_gray'):
                title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
            else:
                title = tr.select_one('td:nth-of-type(3) > div > div > span').get_text(strip=True)
            # artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(
            #     strip=True)
            # album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)
            album_source = tr.select_one('td:nth-of-type(5) a')
            r1 = re.compile(r'\'.*\'(.*)\'', re.DOTALL)
            album_id = re.search(r1, str(album_source)).group(1)

            song_info_list.append({
                'title': title,
                'song_id': song_id,
                'album_id': album_id
            })
        context['song_info_list'] = song_info_list

    return render(request, 'song/song_search_from_melon.html', context)

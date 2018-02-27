import re

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

from crawler.utils.parsing import get_dict_from_dl
from ...models import Album

__all__ = (
    'album_search_from_melon',
)


def album_search_from_melon(request):
    keyword = request.GET.get('keyword')
    context = {}
    if keyword:
        album_info_list = []
        url = 'https://www.melon.com/search/album/index.htm'
        params = {
            'q': keyword,
        }
        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')

        for li in soup.select('div.list_album11.d_album_list > ul > li'):
            dl = li.select_one('div.wrap_album04')
            href = li.select_one('a.thumb').get('href')
            p = re.compile(r"goAlbumDetail\('(\d+)'\)")
            album_id = re.search(p, href).group(1)

            title = dl.select_one('div.atist_info').select_one('dt:nth-of-type(1) > a').get_text(strip=True)
            url_img_cover = dl.select_one('a.thumb img').get('src')
            release_date = dl.select_one('div.atist_info').select_one('dd.wrap_btn').select_one(
                'span.cnt_view').get_text(strip=True)

            album_info_list.append({
                'title': title,
                'url_img_cover': url_img_cover,
                'release_date': release_date,
                'album_id': album_id,
                'is_update': Album.objects.filter(melon_id=album_id).exists(),
            })
        context['album_info_list'] = album_info_list
    return render(request, 'album/album_search_from_melon.html', context)

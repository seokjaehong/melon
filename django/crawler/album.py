import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from crawler.utils.parsing import get_dict_from_dl


class AlbumData:
    def __init__(self, album_id):
        self.album_id = album_id
        self.title = None
        self.url_img_cover = None
        # self.release_date = None
        # self.publisher = None
        # self.agency = None
        self.meta_dict = None

    def get_detail(self):
        url = 'https://www.melon.com/search/album/index.htm'
        params = {
            'q': self.title,
        }
        context = {}
        album_info_list = []

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

            # album_info_list.append({
            #     'title': title,
            #     'url_img_cover': url_img_cover,
            #     'release_date': release_date,
            #     'album_id': album_id,
            #     # 'is_update': Album.objects.filter(melon_id=album_id).exists(),
            # })

    @property
    def release_date(self):
        try:
            return datetime.strptime(self.meta_dict.get('발매일'), '%Y.%m.%d')
        except:
            return

    @property
    def publisher(self):
        return self.meta_dict.get('발매사')

    @property
    def agency(self):
        return self.meta_dict.get('기획사')
import re
import requests
from bs4 import BeautifulSoup, NavigableString

__all__ = (
    'AlbumData',
)


class AlbumData:
    def __init__(self, album_id, title='', img_cover='', release_date=''):
        self.album_id = album_id
        self.title = title
        self.img_cover = img_cover
        self._release_date = release_date

    def __str__(self):
        return f'{self.title} (발매일: {self.release_date})'

    def get_detail(self):
        """
        자신의 _release_date, _lyrics, _genre, _release_date를 채운다
        :return:
        """
        url = f'https://www.melon.com/album/detail.htm'
        params = {
            'albumId': self.album_id,
        }
        response = requests.get(url, params)
        source = response.text
        soup = BeautifulSoup(source, 'lxml')

        div_entry = soup.find('div', class_='entry')
        title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()

        album_img = soup.find('div', class_='thumb').find('a').find('img')
        album_id = re.search(r'images.*?\/.*\/(.*)\_', str(album_img)).group(1)

        info = soup.select_one('div.section_info')
        src = info.select_one('div.thumb img').get('src')
        img_cover = re.search(r'(.*?)/melon/quality.*', src).group(1)

        # artist = div_entry.find('div', class_='artist').get_text(strip=True)
        # artist_id_href = div_entry.select_one('a.artist_name').get('href')
        # artist_id = re.search(r"Detail\('(\d+)'\)", artist_id_href).group(1)

        # 앨범, 발매일, 장르...에 대한 Description list
        dl = div_entry.find('div', class_='meta').find('dl')
        # isinstance(인스턴스, 클래스(타입))
        # items = ['앨범', '앨범명', '발매일', '발매일값', '장르', '장르값']

        # dt, dd목록에서 dd는 get_text()가 아닌 요소 자체를 리스트에 추가
        items = [item if item.name == 'dd' else item.get_text(strip=True) for item in dl.contents if
                 not isinstance(item, str)]
        it = iter(items)
        description_dict = dict(zip(it, it))

        # dd부분 (dict.get() 한 결과)는 Tag이므로 텍스트 가져올땐 get_text(), album_id가져올땐 a태그의 href를 사용
        # album = description_dict.get('앨범').get_text(strip=True)
        # album_id_href = description_dict.get('앨범').select_one('a').get('href')
        # album_id = re.search(r"Detail\('(\d+)'\)", album_id_href).group(1)
        release_date = description_dict.get('발매일').get_text(strip=True)
        # genre = description_dict.get('장르').get_text(strip=True)

        # 리턴하지말고 데이터들을 자신의 속성으로 할당
        self.title = title
        self.album_id = album_id
        self._release_date = release_date
        self.img_cover = img_cover

    @property
    def release_date(self):
        # 만약 가지고 있는 발매일정보가 없다면
        if self._release_date is None:
            # 받아와서 할당
            self.get_detail()
        # 그리고 발매일정보 출력
        return self._release_date

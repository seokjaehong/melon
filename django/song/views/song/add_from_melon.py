import re

import requests
from bs4 import BeautifulSoup, NavigableString
from django.shortcuts import redirect

from album.models import Album
from artist.models import Artist
from ...models import Song

__all__ = (
    'song_add_from_melon',
)


def song_add_from_melon(request):
    # artist_add_from_melon과 같은 기능을 함
    # song_search_from_melon도 같이 구현
    # -> 이 안에 'DB에 추가'하는 Form 구현
    url = f'https://www.melon.com/song/detail.htm'
    song_id = request.POST['song_id']
    params = {
        'songId': song_id,
    }
    response = requests.get(url, params)
    source = response.text
    soup = BeautifulSoup(source, 'lxml')

    div_entry = soup.find('div', class_='entry')
    title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
    dl = div_entry.find('div', class_='meta').find('dl')
    # isinstance(인스턴스, 클래스(타입))
    # items = ['앨범', '앨범명', '발매일', '발매일값', '장르', '장르값']
    items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
    it = iter(items)
    description_dict = dict(zip(it, it))
    genre = description_dict.get('장르')
    # album = description_dict.get('앨범')

    album = dl.find('dd').find('a')
    r1 = re.compile(r'\'(.*)\'', re.DOTALL)
    album_melon_id = re.search(r1, str(album)).group(1)
    album_values = Album.objects.filter(melon_id=album_melon_id).values()

    artist = div_entry.find('div', class_='artist'.find('a', class_='artist_name'))
    r2 = re.compile(r'goArtistDetail(.*)\'(.*?)\'', re.DOTALL)
    artist_melon_id = re.search(r2, str(artist)).group(1)
    artist_values = Artist.objects.filter(melon_id=artist_melon_id).values()
    artist_id = artist_values[0]['id']

    print(album_melon_id)
    print(artist_id)

    try:
        artist_id = artist_values[0]['id']
    except IndexError:
        artist_id = None

    # album에 없는 song이라도 저장할 수 있도록, 더좋은 방법 없나..
    try:
        album_id = album_values[0]['id']
    except IndexError:
        album_id = None

    # if album_set[0]['id'] != []:
    #     album_id = album_values[0]['id']
    # else:
    #     album_id = ''

    if soup.find('div', id='d_video_summary') is not None:
        div_lyrics = soup.find('div', id='d_video_summary')
        lyrics_list = []
        for item in div_lyrics:
            if item.name == 'br':
                lyrics_list.append('\n')
            elif type(item) is NavigableString:
                lyrics_list.append(item.strip())
        lyrics = ''.join(lyrics_list)
    else:
        lyrics = ''

    song, _ = Song.objects.update_or_create(
        melon_id=song_id,
        album_id=album_id,
        title=title,
        genre=genre,
        lyrics=lyrics,
    )
    return redirect('song:song-list')

    # url_img_cover = request.POST['url_img_cover']

from datetime import datetime
from io import BytesIO

import requests
from django.core.files import File
from django.shortcuts import redirect

from artist.models import Artist
from crawler.artist import ArtistData
from crawler.song import SongData
from ...models import Song

__all__ = (
    'song_add_from_melon',
)


def song_add_from_melon(request):
    if request.method == 'POST':
        song_id = request.POST['song_id']

        # 생성된 Song의 artists필드에 연결된 Artist를 추가
        Song.objects.update_or_create_from_melon(song_id)

        # song.artists.add(artist)
        return redirect('song:song-list')

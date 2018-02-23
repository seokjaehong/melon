from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
from django.core.files import File
from django.db import models

from crawler.album import AlbumData
from utils.file import download, get_buffer_ext


class AlbumManager(models.Manager):
    def update_or_create_from_melon(self, album_id):
        album_data = AlbumData(album_id)
        album_data.get_detail()

        album_id = album_data.album_id
        title = album_data.title
        url_img_cover = album_data.img_cover
        release_date_str = album_data.release_date

        album, album_created = self.update_or_create(
            melon_id=album_id,
            defaults={
                'title': title,
                'release_date': datetime.strptime(
                    release_date_str, '%Y.%m.%d') if release_date_str else None,
            }
        )

        temp_file = download(url_img_cover)

        file_name = '{artist_id}.{ext}'.format(
            album_id=album_id,
            ext=get_buffer_ext(temp_file),
        )

        album.img_cover.save(file_name, File(temp_file))
        return album, album_created


class Album(models.Model):
    melon_id = models.CharField('멜론 Album ID', max_length=20, blank=True, null=True, unique=True)
    title = models.CharField(
        '앨범명',
        max_length=100,
    )
    img_cover = models.ImageField(
        '커버 이미지',
        upload_to='album',
        blank=True,
    )
    release_date = models.DateField()

    @property
    def genre(self):
        # 장르는 가지고 있는 노래들에서 가져오기
        # ex) Ballad, Dance
        return ', '.join(self.song_set.values_list('genre', flat=True).distinct())

    objects = AlbumManager()

    def __str__(self):
        # return '{title} [{artists}]'.format(
        #     title=self.title,
        #     artists=', '.join(self.artists.values_list('name', flat=True)),
        # )
        return self.title

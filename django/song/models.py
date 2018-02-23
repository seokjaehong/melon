from django.db import models

from album.models import Album
from artist.models import Artist
from album.models import Album
from crawler.song import SongData


class SongManager(models.Manager):
    def update_or_create_from_melon(self, song_id):
        """
        song_id에 해당하는 Song정보를 멜론 사이트에서 가져와 update_or_create를 실행
        이때 해당 Song의 Artist정보도 가져와서 ArtistManager.update_or_create_from_melon도 실행
        :param song_id: 멜론 사이트에서의 곡의 고유Id
        :return: (song instance, Bool(Song created)
        """
        song_data = SongData(song_id)
        song_data.get_detail()

        # artist, _ = Artist.objects.update_or_create_from_melon(song.artist_id)

        # 생성된 Song의 artists필드에 연결된 Artist를 추가
        artist, _ = Artist.objects.update_or_create_from_melon(song_data.artist_id)
        album, _ = Album.objects.update_or_create_from_melon(song_data.album_id)
        song, song_created = self.update_or_create(
            melon_id=song_id,
            album=album,
            defaults={
                'title': song_data.title,
                'genre': song_data.genre,
                'lyrics': song_data.lyrics,

            }
        )
        song.artists.add(artist)
        # song.album.filter(album=None).update(album_id=album.pk)
        # song.album.add(album.id)
        return song, song_created


class Song(models.Model):
    melon_id = models.CharField('멜론 Song ID', max_length=20, blank=True, null=True, unique=True)
    album = models.ForeignKey(
        Album,
        verbose_name='앨범',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        # default=list,
    )
    artists = models.ManyToManyField(
        Artist,
        verbose_name='아티스트 목록',
        blank=True,
    )
    title = models.CharField(
        '곡 제목',
        max_length=100,
    )
    genre = models.CharField(
        '장르',
        max_length=100,
    )
    lyrics = models.TextField(
        '가사',
        blank=True,
    )

    @property
    def release_date(self):
        # self.album의 release_date를 리턴
        return self.album.release_date

    @property
    def formatted_release_date(self):
        return self.release_date.strftime('%Y.%m.%d')

    def __str__(self):
        # 가수명 - 곡제목 (앨범명)
        # TWICE(트와이스) - Heart Shaker (Merry & Happy)
        # 휘성, 김태우 - 호호호빵 (호호호빵)
        #  artists는 self.album의 속성
        # if self.album:
        #     return '{artists} - {title} ({album})'.format(
        #         artists=', '.join(self.album.artists.values_list('name', flat=True)),
        #         title=self.title,
        #         album=self.album.title,
        #     )
        return self.title

    objects = SongManager()

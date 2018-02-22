from django.db import models

from artist.models import Artist


class Album(models.Model):
    title = models.CharField(
        '앨범명',
        max_length=100,
    )
    melon_id = models.CharField(
        '멜론 Album ID',
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )
    img_cover = models.ImageField(
        '커버 이미지',
        upload_to='album',
        blank=True,
    )
    # artists = models.ManyToManyField(
    #     Artist,
    #     verbose_name='아티스트 목록',
    # )
    release_date = models.DateField()

    @property
    def genre(self):
        # 장르는 가지고 있는 노래들에서 가져오기
        genre = ','.join(self.songs.values_list('genre', flat=True).disctinct()),
        return genre

    def __str__(self):
          return self.title
#     return '{title} [{artists}]'.format(
#         title=self.title,
#         artists=', '.join(self.artists.values_list('name', flat=True)),
#     )

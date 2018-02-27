from datetime import datetime
from django.core.files import File
from django.db import models

from config import settings
from crawler.album import AlbumData

from utils.file import download, get_buffer_ext

User = settings.AUTH_USER_MODEL


class AlbumManager(models.Manager):
    def update_or_create_from_melon(self, album_id):
        album_data = AlbumData(album_id)
        album_data.get_detail()

        album_id = album_data.album_id
        title = album_data.title
        url_img_cover = album_data.url_img_cover
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

        file_name = '{album_id}.{ext}'.format(
            album_id=album_id,
            ext=get_buffer_ext(temp_file),
        )
        # 중복데이터 제거
        if album.img_cover:
            album.img_cover.delete()
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
        return self.title

    def toggle_like_user(self, user):
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        if not like_created:
            like.delete()
        return like_created

    class Meta:
        verbose_name_plural = 'Melon-Album'


class AlbumLike(models.Model):
    # album와 User(members.User)와의 관계를 나타내는 중개모델
    album = models.ForeignKey(
        Album,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,

    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_album_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return 'Albumlike (User: {user}, Album{album}), Created{created}'.format(
            # return '"{album}"가수의 좋아요를 누른({username}, {date})'.format(
            album=self.album.name,
            user=self.user.username,
            created=datetime.strftime(self.created_date, '%y.%m.%d'),
        )

    class Meta:
        unique_together = (
            ('album', 'user'),
        )
        # 좋아요가 중복으로 되는것을 방지

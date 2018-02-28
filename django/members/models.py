from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from artist.models import ArtistLike


class User(AbstractUser):
    # user class 추가
    # settings.py > installed_apps에 members application 추가
    # settings.py AUTH_USER_MODELS 정의( AppName.ModelClassName)
    # 모든 application들의 migration 삭제

    # makemigrations  ->  migrate

    img_profile = models.ImageField(
        upload_to='user',
        blank=True
    )

    def toggle_like_artist(self, artist):
        """
        이 user와 특정 artist를 연결하는 중개모델인 ArtistLike 인스턴스를
        없을 경우 생성, 있으면 삭제 하는 매서드

        :param user:
        :return:
        """
        #
        # if ArtistLike.objects.filter(artist=artist):
        #     ArtistLike.objects.filter(artist=artist, user=self.user).delete()
        # else:
        #     ArtistLike.objects.create(
        #         artist=artist,
        #         user=self.user,
        #     )
        like, like_created = self.like_artist_info_list.get_or_create(artist=artist)
        if not like_created:
            like.delete()
        return like_created

    def toggle_like_album(self, album):
        like, like_created = self.like_album_info_list.get_or_create(album=album)
        if not like_created:
            like.delete()
        return like_created

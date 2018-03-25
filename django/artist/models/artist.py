import json

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields.files import FieldFile
from django.forms import model_to_dict

from .artist_youtube import ArtistYouTube
from .managers import ArtistManager
from config import settings

User = settings.AUTH_USER_MODEL

__all__ = (
    'Artist',
)


class Artist(models.Model):
    BLOOD_TYPE_A = 'a'
    BLOOD_TYPE_B = 'b'
    BLOOD_TYPE_O = 'o'
    BLOOD_TYPE_AB = 'c'
    BLOOD_TYPE_OTHER = 'x'
    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_AB, 'AB형'),
        (BLOOD_TYPE_OTHER, '기타'),
    )
    melon_id = models.CharField(
        '멜론 Artist ID',
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='artist',
        blank=True,
    )
    name = models.CharField(
        '이름',
        max_length=50,
    )
    real_name = models.CharField(
        '본명',
        max_length=30,
        blank=True,
    )
    nationality = models.CharField(
        '국적',
        max_length=50,
        blank=True,
    )
    birth_date = models.DateField(
        '생년월일',
        blank=True,
        null=True,
    )
    constellation = models.CharField(
        '별자리',
        max_length=30,
        blank=True,
    )
    blood_type = models.CharField(
        '혈액형',
        max_length=1,
        choices=CHOICES_BLOOD_TYPE,
        blank=True,
    )
    intro = models.TextField(
        '소개',
        blank=True,
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ArtistLike',
        related_name='like_artists',
        blank=True
    )
    youtube_videos = models.ManyToManyField(
        ArtistYouTube,
        related_name='artists',
        blank=True,
    )

    objects = ArtistManager()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name

    def toggle_like_user(self, user):
        """
        자신의 like_users에 주어진 user가 존재하지 않으면
            like_users에 추가한다
        만약 이미 존재하면 없앤다.
        :param user:
        :return:
        """
        # query = ArtistLike.objects.filter(user=user,artist=self)
        # if query.exists():
        #     query.delete()
        #     return False
        # else:
        #     ArtistLike.objects.create(
        #         artist=self,
        #         user=user,
        #     )
        #     return True
        #
        # 자신이 'artist'이며 user가 주어진 user인 ArtistlLike를 가져오거나 없으면 생성
        like, like_created = self.like_user_info_list.get_or_create(user=user)
        if not like_created:
            like.delete()
        return like_created

    def to_json(self):

        # model_to_dict의 결과가 dic
        # 해당 dict의 item을 순회하며
        # json serialize할 때 나는 에러타입의 value를
        # 적절히 변환해서 value에 다시 대입
        user_class = get_user_model()
        ret = model_to_dict(self)

        def convert_value(value):
            if isinstance(value, FieldFile):
                return value.url if value else None
            elif isinstance(value, user_class):
                return value.pk
            elif isinstance(value, ArtistYouTube):
                return value.pk
            return value

        def convert_obj(obj):
            if isinstance(obj, list):
                for index, item in enumerate(obj):
                    obj[index] = convert_obj(item)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    obj[key] = convert_obj(value)
            return convert_value(obj)

        convert_obj(ret)
        return ret

    class Meta:
        verbose_name_plural = 'Melon-Artist'

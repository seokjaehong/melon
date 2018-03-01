from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import requests
from django.core.files import File
from django.db import models

from .artist import Artist
from config import settings
from crawler.artist import ArtistData

User = settings.AUTH_USER_MODEL
# from members.models import User

from utils.file import download, get_buffer_ext

__all__= (
    'ArtistLike',
)

class ArtistLike(models.Model):
    # Artist와 User(members.User)와의 관계를 나타내는 중개모델
    artist = models.ForeignKey(
        Artist,
        related_name='like_user_info_list',
        on_delete=models.CASCADE,

    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='like_artist_info_list',
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return 'Artistlike (User: {user}, Artist{artist}), Created{created}'.format(
            # return '"{artist}"가수의 좋아요를 누른({username}, {date})'.format(
            artist=self.artist.name,
            user=self.user.username,
            created=datetime.strftime(self.created_date, '%y.%m.%d'),
        )

    class Meta:
        unique_together = (
            ('artist', 'user'),
        )
        # 좋아요가 중복으로 되는것을 방지

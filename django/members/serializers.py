from django.contrib.auth import get_user_model
from rest_framework import serializers

from artist.models import Artist, ArtistYouTube

User = get_user_model()

__all__ = (
    'UserSerializer',
)


# user시리얼라이저 할때는 __all__쓰지말자.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
        )

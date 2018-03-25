import requests
from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers

from artist.models import Artist, ArtistYouTube

User = get_user_model()


# __all__ = (
#     'UserSerializer',
# )


# user시리얼라이저 할때는 __all__쓰지말자.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
        )


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        if access_token:
            user = authenticate(access_token=access_token)
            # authenticate가 backend에 2개가 있는데 넘겨주는 키워드를 가지고 구분해서 호출하게 된다.
            if not user:
                raise serializers.ValidationError('액세스 토큰이 잘못됬습니다.')
        else:
            raise serializers.ValidationError('액세스 토큰이 필요해요')

        attrs['user'] = user
        return attrs
        # if access_token:
        #     params = {
        #         'access_token': access_token,
        #         'fields': ','.join([
        #             'id',
        #             'name',
        #             'picture.width(2500)',
        #             'first_name',
        #             'last_name',
        #         ])
        #     }
        #     response = requests.get('https://graph.facebook.com/v2.12/me', params)
        #     user_info = response.json()
        #
        #     facebook_id = user_info['id']
        #     first_name = user_info['first_name']
        #     last_name = user_info['last_name']
        #     # url_picture = user_info['picture']['data']['url']
        #
        #     try:
        #         user, _ = User.objects.get(username=facebook_id)
        #     except:
        #         user = User.objects.create_user(
        #             username=facebook_id,
        #             first_name=first_name,
        #             last_name=last_name,
        #             # url_picture=url_picture,
        #         )
        # else:
        #     raise serializers.ValidationError('액세스 토큰이 필요함')
        #

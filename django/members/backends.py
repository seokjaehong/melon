from django.contrib.auth import get_user_model
from django.core.files import File

from config import settings
import requests

from utils.file import download, get_buffer_ext

User = get_user_model()


class FacebookBackends:
    CLIENT_ID = settings.FACEBOOK_APP_ID
    CLIENT_SECRET = settings.FACEBOOK_SECRET_CODE
    URL_ACCESS_TOKEN = 'https://graph.facebook.com/v2.12/oauth/access_token'
    URL_ME = 'https://graph.facebook.com/v2.12/me'

    def authenticate(self, request, code):
        def get_access_token(auth_code):
            """
            user가 facebook에서 melon 어플리케이션의 사용에 대해 '승인'한 경우
            facebook에서 melon 어플리케이션의 주소(redirect_uri)에 'code'라는 GET parameter로 전해주는
            인증코드(auth_code)를 사용해서
            페이스북 GraphAPI에 access_token요청, 결과를 가져와 리

            :param auth_code: 유저가 페이스북에 로그인/앱 승인한 결과로 돌아오는 'code' GET parameter
            :return:
            """
            redirect_uri = "http://localhost:8000/facebook-login/"
            params_access_token = {
                'client_id': self.CLIENT_ID,
                'redirect_uri': redirect_uri,
                'client_secret': self.CLIENT_SECRET,
                'code': auth_code,
            }
            response = requests.get(self.URL_ACCESS_TOKEN, params_access_token)
            response_dict = response.json()
            return response_dict['access_token']

        def get_user_info(user_access_token):
            """
            User access token을 사용해서 GraphAPI의 'User'항목을 리턴
            (엔드포인트 'me'를 사용해서 access_token에 해당하는 사용자의 정보를 가져옴)
            :param user_access_token: 정보를 가져올 facebook user access token
            :return: User 정보(dict)
            """
            params = {
                'access_token': user_access_token,
                'fields': ','.join([
                    'id',
                    'name',
                    'picture.width(2500)',
                    'first_name',
                    'last_name',
                ])
            }

            response = requests.get(self.URL_ME, params)
            response_dict = response.json()
            return response_dict

        # {'id': '1746683798704556', 'name': 'S eokJae Hong', 'picture': {'data': {'height': 1079, 'is_silhouette': False, 'url': 'https://scontent.xx.fbcdn.net/v/t31.0-1/16904750_1386387041400902_7254244577969287703_o.jpg?oh=4bfe02828716d67e65fa5b422f32c6a3&oe=5B0B6A0E', 'width': 1092}}, 'first_name': 'SeokJae', 'last_name': 'Hong'}

        try:
            access_token = get_access_token(code)
            user_info = get_user_info(access_token)

            facebook_id = user_info['id']
            name = user_info['name']
            first_name = user_info['first_name']
            last_name = user_info['last_name']
            url_picture = user_info['picture']['data']['url']

            try:
                user = User.objects.get(username=facebook_id)
            except:
                user = User.objects.create_user(
                    username=facebook_id,
                    first_name=first_name,
                    last_name=last_name,
                )

            temp_file = download(url_picture)

            file_name = '{username}.{ext}'.format(
                username=facebook_id,
                ext=get_buffer_ext(temp_file),
            )
            if user.img_profile:
                user.img_profile.delete()
            user.img_profile.save(file_name, File(temp_file))

            return user
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

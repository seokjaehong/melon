# from config import settings
import requests
from django.conf import settings
# from config import settings
from django.contrib.auth import get_user_model, login, authenticate

from django.http import HttpResponse
from django.shortcuts import redirect

__all__ = (
    'facebook_login',
)

User = get_user_model()

def facebook_login(request):
    # GET parameter가 왔을 것으로 가정하고
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    # print(user)
    login(request, user)
    return redirect('index')


def facebook_login_backup(request):
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CODE
    code = request.GET['code']
    redirect_uri = "http://localhost:8000/facebook-login/"
    url = ' https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.get(url, params)
    response_dict = response.json()
    # print(response_dict)
    for key, value in response_dict.items():
        print(f'{key} : {value}')
    # me 엔드포인트에 get요청 보내기

    url = 'https://graph.facebook.com/v2.12/me'
    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'picture.width(2500)',
            'first_name',
            'last_name',
        ])
    }
    response = requests.get(url, params)
    response_dict = response.json()

    # {'id': '1746683798704556', 'name': 'SeokJae Hong', 'picture': {'data': {'height': 1079, 'is_silhouette': False, 'url': 'https://scontent.xx.fbcdn.net/v/t31.0-1/16904750_1386387041400902_7254244577969287703_o.jpg?oh=4bfe02828716d67e65fa5b422f32c6a3&oe=5B0B6A0E', 'width': 1092}}, 'first_name': 'SeokJae', 'last_name': 'Hong'}

    facebook_id = response_dict['id']
    name = response_dict['name']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_picture = response_dict['picture']['data']['url']

    #facebook_id가 username인 User가 존재하는경우

    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)

    # return HttpResponse(str(response_dict))
    else:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
    login(request, user)
    return redirect('index')

    # access_token : EAANlZCs5UIUIBALSsmWjRnYl4i6XXSt9uzmNh5j7rcyBZCH92K54ukKNssuoS6p1NJvC8zZBpdkn9qLInrZBeWTwJX2EsVBREXq2vveGzlzDpo5NLkpoZAcGyKc4INEXXA83ZCGwTLeDVTQOMbFoTIlNwBgRpVoroG1TBl9gFhVgZDZD
    #AIzaSyDsdhEKBzSrFOzmEPqe-xsVtrBiMEJ6TZg
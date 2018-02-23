from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    # user class 추가
    # settings.py > installed_apps에 members application 추가
    # settings.py AUTH_USER_MODELS 정의( AppName.ModelClassName)
    # 모든 application들의 migration 삭제

    # makemigrations  ->  migrate

    pass

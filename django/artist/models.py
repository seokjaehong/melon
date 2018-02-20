from django.db import models
from django.forms import forms
#from django_extensions import settings


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
    melon_id =models.CharField(
        '멜론 Artist ID',
        max_length=20,
        blank=True,
        unique=True,
        #  melon_id가 중복으로 들어와있는경우 에러가 나기때문에 unique를 추가해주는데
        # 기존 data에 대해 업데이트를 해주어야함 그래서 null=True를 먼저 허용해서 makemigration하고,
        # shell: Artist.objects.filter(melon_id='').update(melon_id=None)

        null =True,
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
        # input_formats=settings.DATE_INPUT_FORMATS
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

    def __str__(self):
        return self.name

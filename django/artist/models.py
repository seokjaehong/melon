from django.db import models

# Create your models here.
class Artist(models.Model):
    BLODD_TYPE_A = 'a'
    BLODD_TYPE_B = 'b'
    BLODD_TYPE_O = 'o'
    BLODD_TYPE_AB = 'c'
    BLODD_TYPE_OTHER ='x'
    CHOICE_BLOOD_TYPE = (
        (BLODD_TYPE_A,'A형'),
        (BLODD_TYPE_B,'B형'),
        (BLODD_TYPE_AB,'AB형'),
        (BLODD_TYPE_O,'O형'),
        (BLODD_TYPE_OTHER,'기타'),
    )
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='artist',
    )
    name = models.CharField(
        '이름',
        max_length=50
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
    birth_date = models.DateTimeField(
        '생년월일',
        blank=True,
        null=True,
    )
    constellation = models.CharField(
        '별자리',
        max_length=30,
    )
    broodtype = models.CharField(
        '혈액형',
        max_length=1,
        choices=CHOICE_BLOOD_TYPE,
        blank=True,
    )

    def __str__(self):
        return self.name
# Generated by Django 2.0.2 on 2018-02-23 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('melon_id', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='멜론 Album ID')),
                ('title', models.CharField(max_length=100, verbose_name='앨범명')),
                ('img_cover', models.ImageField(blank=True, upload_to='album', verbose_name='커버 이미지')),
                ('release_date', models.DateField()),
            ],
        ),
    ]

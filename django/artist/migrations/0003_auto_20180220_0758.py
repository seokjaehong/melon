# Generated by Django 2.0.2 on 2018-02-20 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0002_artist_melon_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='melon_id',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='멜론 Artist ID'),
        ),
    ]

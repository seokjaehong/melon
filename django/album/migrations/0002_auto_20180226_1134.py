# Generated by Django 2.0.2 on 2018-02-26 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name_plural': 'Melon-Album'},
        ),
        migrations.AddField(
            model_name='albumlike',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_user_info_list', to='album.Album'),
        ),
        migrations.AddField(
            model_name='albumlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_album_info_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='albumlike',
            unique_together={('album', 'user')},
        ),
    ]

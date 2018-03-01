from django.forms import ModelForm
from django import forms

from artist.models import Artist, ArtistYouTube

__all__ = (
    'ArtistForm',
    # 'YoutubeForm',
)


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['img_profile', 'name', 'real_name', 'nationality', 'birth_date', 'constellation', 'blood_type',
                  'intro']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }


# class YoutubeForm(forms.ModelForm):
#     class Meta:
#         model = ArtistYouTube
#         fields = ['youtube_id', 'title', 'url_thumbnail']
#         widgets = {
#             'name': forms.TextInput(
#                 attrs={
#                     'class': 'form-control'
#                 }
#
#             )
#         }

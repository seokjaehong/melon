from django.forms import ModelForm
from django import forms

from album.models import Album

__all__ = (
    'AlbumForm'
)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'img_cover', 'release_date']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

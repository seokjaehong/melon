from django import forms

__all__ = (
    'UploadFileForm',
)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

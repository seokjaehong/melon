from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

__all__ = (
    'SignupForm'
)


# required=False 는 blank=True 와 같은 내용

class SignupForm(forms.Form):
    username = forms.CharField(label='아이디', required=False)
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError('이미사용중인아이디입니다. ')
        return data

    # 읽어오는 순서가 username, password, password2 순서로 읽어오기 떄문에
    # clean_password로 하면 password2를 읽어오지 못한다.
    # 그래서 clean_password2 로 이름을 해줘야함

    def clean_password2(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise ValidationError('비밀번호와 비밀번호 확인란의 값이 다릅니다. ')
        return password1

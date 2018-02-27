from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from members.forms import SignupForm

User = get_user_model()

__all__= (
    'logout_view',
)

def logout_view(request):
    # /logout/
    # 문서에서 logout <- django logout 검색
    # GET요청이든 POST요청이든 상관없음
    logout(request)
    return redirect('index')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


# Create your views here.

def login_view(request):
    # POST요청일때는
    # authenticate -> login 후 'index' 로 redirect

    # GET요청일 떄는
    # members/login.html 파일을 보여줌
    # 해당 파일 form에는 username, password input과 '로그인 버튼이 있음
    # form 은 method POST로 다시 이 view로의 action(빈 값을 가짐)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('index')
    return render(request, 'members/login.html')

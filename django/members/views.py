from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from members.forms import SignupForm

User = get_user_model()


def login_view(request):
    # POST요청일때는
    # authentictate -> login후 'index'로 redirect
    #   실패시에는 다시 GET요청의 로직으로 이동
    #
    # GET요청일때는
    # members/login.html파일을 보여줌
    #   해당 파일의 form에는 username, password input과 '로그인'버튼이 있음
    #   form은 method POST로 다시 이 view로의 action(빈 값)을 가짐
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'members/login.html')


def logout_view(request):
    # /logout/
    # 문서에서 logout <- django logout 검색
    # GET요청이든 POST요청이든 상관없음
    logout(request)
    return redirect('index')


def signup_view(request):
    # /signup/
    # username, password, password2가 전달되었다는 가정
    # username이 중복되는지 검사, 존재하지않으면 유저 생성 후 index로 이동
    #   password, password2가 같은지도 확인
    # 이외의경우는 다시 회원가입화면으로
    context = {
        'errors': [],
        # 'form':SignupForm,
    }
    # signupForm 인스턴스 생성
    # context에 인스턴스를 전달
    # 전달받은 변수를 템플리셍서 변수 렌드링
    signup_form = SignupForm()
    context['signup_form'] = signup_form

    # 전달받은 데이터에 문제가 있을 경우, context['errors']를 채우고
    # 해당 내용을 signup.html템플릿에서 출력
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # 여기에서 validation이 이루어짐
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # password2 = form.cleaned_data['password2']
            # is_valid = True

            # if User.objects.filter(username=username).exists():
            #     form.add_error('username', '이미 사용되고 있는 아이디입니다')
            #     is_valid=False
            # if password != password2:
            #     form.add_error('password2', '비밀번호와 비밀번호 확인란의 값이 다릅니다. ')
            #     is_valid = False
            # if is_valid:
            User.objects.create_user(username=username, password=password)
            return redirect('index')
    else:
        form = SignupForm()
    context = {
        'signup_form': form,
    }
    return render(request, 'members/signup.html', context)

    # username = request.POST['username']
    # password = request.POST['password']
    # password2 = request.POST['password2']
    #
    # is_valid = True
    # if User.objects.filter(username=username).exists():
    #     context['errors'].append('Username already exists')
    #     is_valid = False
    # if password != password2:
    #     context['errors'].append('Password and Password2 is not equal')
    #     is_valid = False
    # if is_valid:
    #     User.objects.create_user(username=username, password=password)
    #     return redirect('index')

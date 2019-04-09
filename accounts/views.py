from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(request):
    if request.method  == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return redirect('/feeds')
    return render(request, 'accounts/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/accounts/login')
    else:
        return render(request, 'accounts/logout.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/feeds')
        else:
            return render(request, 'accounts/login.html', {'error' : 'Hey! username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def profile(request):
    if request.method == 'POST':
        # 나중에... 비번 확인하는 로직도 넣자
        tmp_password = request.POST['password']
        profile.user.username = request.POST['username']
        profile.user.set_password(tmp_password)

        profile.save
        return redirect('/feeds')
    else:
        return render(request, 'accounts/profile.html')
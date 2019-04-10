from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile

# Create your views here.
def signup(request):
    if request.method  == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return redirect('/feeds')
        else:
            return render(request, 'accounts/signup.html', {'error' : 'Check your password'})
    else:
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
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        current_password = request.POST['current_password']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if user.check_password(current_password) and (password1 == password2) and (password1 != '') :
            # good case
            user.set_password(password1)
            user.username = request.POST['username']
            user.save()
            profile.college = request.POST['college']
            profile.major = request.POST['major']
            profile.save()
            return redirect('/feeds')

        else:
            # for error message
            if user.check_password(current_password) == False :
                error_msg = 'Check your current password'
            elif password1 != password2 :
                error_msg = 'Check your new password'
            elif password1 == '' :
                error_msg = 'Check your new password. It is empty value!'
            else :
                error_msg = 'Unexpected error! Please tell us about this error case'
            return render(request, 'accounts/profile.html', {'profile': profile, 'error': error_msg})

    return render(request, 'accounts/profile.html', {'profile': profile}) #for GET method
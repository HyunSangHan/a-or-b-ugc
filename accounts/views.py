from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth
from django.utils import timezone

# Create your views here.
def signup(request):
    if request.method  == 'POST':
        #이름 겹치면 어떻게 할 건지 정해야됨
        password = request.POST['password1']
        email = request.POST['email']
        if password == request.POST['password2']:
            email_already = User.objects.filter(email=email)
            if email_already.count() > 0:
                return render(request, 'accounts/signup.html', {'error' : 'The email address is already exist'})
            else:
                user = User.objects.create_user(email=email, username=request.POST['username'], password=password)
                profile = user.profile
                # print(profile)
                profile.birthday = request.POST['birthday']
                profile.is_male = request.POST['gender']
                profile.left_level = request.POST['politics']
                profile.region = request.POST['region']
                profile.image = request.FILES.get('profile_image', False)
                profile.save()
                auth.login(request, user)
                return redirect('/feeds')
        else:
            return render(request, 'accounts/signup.html', {'error' : 'Check your password'})
    elif request.user.is_anonymous:
        return render(request, 'accounts/signup.html')
    else:
        return redirect('/feeds/')

def logout(request):
    auth.logout(request)
    next = '/accounts/login'
    return redirect('%s'%next)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            if User.objects.get(email=email):
                username = User.objects.get(email=email).username
                password = request.POST['password']
                user = auth.authenticate(request, username = username, password = password)
                user.profile.recent_login = timezone.now()
                user.profile.save()
                if user is not None:
                    auth.login(request, user)
                    return redirect('/feeds')
                else:
                    return render(request, 'accounts/login.html', {'error' : 'Hey! password is incorrect'})
        except:
            return render(request, 'accounts/login.html', {'error' : 'Hey! email is incorrect'})
    elif request.user.is_anonymous:
        return render(request, 'accounts/login.html')
    else:
        return redirect('/feeds/')

def profile(request):
    # auth.login(request, user)
    if request.method == 'POST':
    #하나씩만 입력해도 되도록.
        user = request.user
        profile = user.profile
        user.username = request.POST['username']
        user.save()
        profile.birthday = request.POST['birthday']
        profile.is_male = request.POST['gender']
        profile.left_level = request.POST['politics']
        profile.region = request.POST['region']
        profile.major = request.POST['major']
        profile.likes_iphone = request.POST['likes_iphone']
        profile.is_premium = True
        profile.save()
        update_session_auth_hash(request, request.user)
        return redirect('/feeds/creator')
    else:
        user = request.user
        social_user = user.socialaccount_set.first()
        social_data = social_user.extra_data
        profile = user.profile
        #첫 로그인인 경우로 조건문 걸어주고
        ## 안된거
        # birthday, is_male, image,
        # left_level, major, 
        # region, likes_iphone, is_premium
        profile.save()
        print(social_user.extra_data)
        # print(social_user.extra_data['properties'])


        return render(request, 'accounts/profile.html', {'profile': profile}) #for GET method
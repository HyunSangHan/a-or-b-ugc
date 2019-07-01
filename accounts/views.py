from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth
from django.utils import timezone
from django.http import JsonResponse, HttpResponse

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
    if request.method == 'POST' and request.is_ajax():
        is_success = True #초기값
        is_new_premium = False
        done_cnt = 0 #넣은 정보 개수 확인용

    #닉네임(아이디)에 대한 로직
        user = request.user
        username = request.POST['username']
        if username != user.username:
            same_name_user = User.objects.filter(username=username)
            import re
            if same_name_user.count() > 0 or re.match("^[가-힣a-zA-Z0-9_.-]+$", username) is None: 
                is_success = False
            elif len(username) > 0:             
                user.username = username
                user.save()
                done_cnt += 1
                is_success = True

                profile = user.profile

                profile_image = request.FILES.get('profile_image', False)
                if profile_image:
                    if profile.image is None:
                        profile.image = profile_image
                    else:
                        if profile_image != profile.image:
                            profile.image = profile_image

                birth = request.POST.get('birth')
                if birth is not None and birth != '' :
                    if int(birth) != profile.birth and int(birth) > 1920 and int(birth) < 2020:
                        profile.birth = int(birth)
                    done_cnt += 1

                is_male = request.POST.get('gender')
                if is_male is not None:
                    if is_male != str(profile.is_male):
                        profile.is_male = is_male
                    done_cnt += 1

                left_level = request.POST.get('politics')
                if left_level is not None:
                    if int(left_level) != profile.left_level and int(left_level) > 0 and int(left_level) < 6:
                        profile.left_level = left_level
                    done_cnt += 1

                region = request.POST.get('region')
                if region is not None:
                    if int(region) != profile.region and int(region) > 0 and int(region) < 9:
                        profile.region = region
                    done_cnt += 1

                religion = request.POST.get('religion')
                if religion is not None:
                    if int(religion) != profile.religion and int(religion) > 0 and int(religion) < 9:
                        profile.religion = religion
                    done_cnt += 1

                major = request.POST.get('major')
                if major is not None and major != "문과" and major != "이과" and major !="예체능":
                    if major != profile.major:
                        profile.major = "기타"
                    done_cnt += 1
                elif major is not None:
                    if major != profile.major:
                        profile.major = major
                    done_cnt += 1

                likes_iphone = request.POST.get('mobile')
                if likes_iphone is not None:
                    if likes_iphone != str(profile.likes_iphone):
                        profile.likes_iphone = likes_iphone
                    done_cnt += 1

                if done_cnt > 7 and profile.is_premium != True:
                    profile.is_premium = True
                    is_new_premium = True 

                profile.save()

                update_session_auth_hash(request, request.user)

        else:
            done_cnt += 1
            profile = user.profile
            profile_image = request.FILES.get('profile_image', False)
            if profile_image:
                if profile.image is None:
                    profile.image = profile_image
                else:
                    if profile_image != profile.image:
                        profile.image = profile_image

            birth = request.POST.get('birth')
            if birth is not None and birth != '' :
                if int(birth) != profile.birth and int(birth) > 1920 and int(birth) < 2020:
                    profile.birth = int(birth)
                done_cnt += 1

            is_male = request.POST.get('gender')
            if is_male is not None:
                if is_male != str(profile.is_male):
                    profile.is_male = is_male
                done_cnt += 1

            left_level = request.POST.get('politics')
            if left_level is not None:
                if int(left_level) != profile.left_level and int(left_level) > 0 and int(left_level) < 6:
                    profile.left_level = left_level
                done_cnt += 1

            region = request.POST.get('region')
            if region is not None:
                if int(region) != profile.region and int(region) > 0 and int(region) < 9:
                    profile.region = region
                done_cnt += 1

            religion = request.POST.get('religion')
            if religion is not None:
                if int(religion) != profile.religion and int(religion) > 0 and int(religion) < 9:
                    profile.religion = religion
                done_cnt += 1

            major = request.POST.get('major')
            if major is not None and major != "문과" and major != "이과" and major !="예체능":
                if major != profile.major:
                    profile.major = "기타"
                done_cnt += 1
            elif major is not None:
                if major != profile.major:
                    profile.major = major
                done_cnt += 1

            likes_iphone = request.POST.get('mobile')
            if likes_iphone is not None:
                if likes_iphone != str(profile.likes_iphone):
                    profile.likes_iphone = likes_iphone
                done_cnt += 1

            if done_cnt > 7 and profile.is_premium != True:
                profile.is_premium = True
                is_new_premium = True 

            profile.save()

            update_session_auth_hash(request, request.user)

        context = {
            'comment': {
                'is_success': is_success,
                'is_new_premium': is_new_premium,
                'rest_info_num': 8 - done_cnt
            }
        }
        return JsonResponse(context)

    elif request.user.is_anonymous:
        return redirect('/accounts/login')

    else:
        user = request.user            
        social_user = user.socialaccount_set.first()
        # social_data = social_user.extra_data
        profile = user.profile
        if profile.is_first_login:
            profile.is_first_login = False
        #첫 로그인인 경우로 조건문 걸어주고
        ## 안된거
        # birthday, is_male, image,
        # left_level, major, 
        # region, likes_iphone, is_premium
        profile.save()
        # print(social_user.extra_data)
        # print(social_user.extra_data['properties'])


        return render(request, 'accounts/profile.html', {'profile': profile}) #for GET method
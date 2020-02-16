from django.shortcuts import render
from .models import Feed, FeedComment, HashTag, TagRelation, Upvote, CommentUpvote, Report, Notification
from accounts.models import Profile, Follow
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from operator import attrgetter
from django.http import JsonResponse, HttpResponse
import json
from .reuse_function import make_notification
from django.utils import timezone
import os
import sys
from snulion7th.settings import IMG_CLIENT_ID, IMG_CLIENT_KEY
import urllib
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
from collections import OrderedDict
import re

NUM_PER_PAGE = 2

def main(request):
    return redirect('/feeds')

def index(request): 
    if request.user.is_anonymous == False and request.user.profile.is_first_login:
        return redirect('/accounts/profile/')
    # print(HashTag.objects.all())
    keyword = request.GET.get('keyword', '')
    feeds_all = Feed.objects.all().order_by('-updated_at', '-created_at')
#TODO: 검색기능 추후 보완 필요
    if keyword: 
        from django.db.models import Q
        #필드에서 피드 뽑아오기
        feeds_by_field = list(feeds_all.filter(Q(title__icontains=keyword) | Q(content_a__icontains=keyword) | Q(content_b__icontains=keyword)))
        #해시태그에서 피드 뽑아오기
        feeds_by_hashtag = []
        tags = HashTag.objects.all().filter(Q(tag__icontains=keyword))
        for tag in tags:
            feeds_by_hashtag = feeds_by_hashtag + list(tag.tagged_feeds.all())
        feeds_all = list(set(feeds_by_field + feeds_by_hashtag))
        feeds_all = sorted(feeds_all, key=lambda x: x.updated_at, reverse=True)
#TODO: 페이지네이션과의 파라미터 조화 필요

    paginator = Paginator(feeds_all, NUM_PER_PAGE)
    page_num = request.GET.get('page')
    feeds = paginator.get_page(page_num)
    search_result_num = len(feeds_all)
    if keyword and feeds:
        is_searched = True
    elif keyword == "":
        is_searched = False
    else:
        is_searched = True
    return render(request, 'feedpage/index.html', {'feeds': feeds, 'keyword': keyword, 'page': page_num, 'is_searched': is_searched, 'search_result_num': search_result_num})

def index_ajax(request): 
    if request.user.is_anonymous == False and request.user.profile.is_first_login:
        return redirect('/accounts/profile/')
    # print(HashTag.objects.all())
    keyword = request.GET.get('keyword', '')
    feeds_all = Feed.objects.all().order_by('-updated_at', '-created_at')
#TODO: 검색기능 추후 보완 필요
    if keyword: 
        from django.db.models import Q
        #필드에서 피드 뽑아오기
        feeds_by_field = list(feeds_all.filter(Q(title__icontains=keyword) | Q(content_a__icontains=keyword) | Q(content_b__icontains=keyword)))
        #해시태그에서 피드 뽑아오기
        feeds_by_hashtag = []
        tags = HashTag.objects.all().filter(Q(tag__icontains=keyword))
        for tag in tags:
            feeds_by_hashtag = feeds_by_hashtag + list(tag.tagged_feeds.all())
        feeds_all = list(set(feeds_by_field + feeds_by_hashtag))
        feeds_all = sorted(feeds_all, key=lambda x: x.updated_at, reverse=True)
#TODO: 페이지네이션과의 파라미터 조화 필요

    paginator = Paginator(feeds_all, NUM_PER_PAGE)
    page_num = int(request.GET.get('page'))
    feeds = paginator.get_page(page_num)
    search_result_num = len(feeds_all)

    if keyword and feeds:
        is_searched = True
    elif keyword == "":
        is_searched = False
    else:
        is_searched = True

    import math
    page_num_max = math.ceil(search_result_num / 2)
    if page_num > page_num_max:
        feeds = None
    return render(request, 'feedpage/index_ajax.html', {'feeds': feeds, 'keyword': keyword, 'page': page_num, 'is_searched': is_searched, 'search_result_num': search_result_num})

def new(request):
    if request.method == 'POST': # create
        title = request.POST['title']
        content_a = request.POST['content_a']
        content_b = request.POST['content_b']
        img_url_a = request.POST.get('img_url_a')
        img_url_b = request.POST.get('img_url_b')
        img_a = request.FILES.get('img_a')
        # img_a = request.POST['test_img_a']
        print(img_a)
        img_b = request.FILES.get('img_b')

        if img_url_a is None and img_a is None:
            print("이미지 A를 누락")
            try:
                next = request.META['HTTP_REFERER']
            except:
                next = '/feeds/'
            return redirect('%s'%next)

        if img_url_b is None and img_b is None:
            print("이미지 B를 누락")
            try:
                next = request.META['HTTP_REFERER']
            except:
                next = '/feeds/'
            return redirect('%s'%next)

        feed = Feed.objects.create(title=title, content_a=content_a, img_a=img_a, img_b=img_b, content_b=content_b, creator=request.user)
        if img_url_a:
            name = urlparse(img_url_a).path.split('/')[-1]
            response = requests.get(img_url_a)
            if response.status_code == 200:
                feed.img_a.save(name, ContentFile(response.content), save=True)
        if img_url_b:
            name = urlparse(img_url_b).path.split('/')[-1]
            response = requests.get(img_url_b)
            if response.status_code == 200:
                feed.img_b.save(name, ContentFile(response.content), save=True)
        hash_tag_raw = request.POST['hash_tag_raw'].replace(" ", "")
        hash_tag_raw_edit = re.sub('[-=./?:$!@\|"^%*&()}{+]', '', hash_tag_raw)
        hash_tag_all = hash_tag_raw_edit.split("#")
        hash_tag_all = list(OrderedDict.fromkeys(hash_tag_all))

        for hash_tag in hash_tag_all:
            if hash_tag != "":
                if HashTag.objects.filter(tag=hash_tag).count() > 0:
                    tag = HashTag.objects.get(tag=hash_tag)
                    TagRelation.objects.create(hash_tag=tag, feed=feed)
                else:
                    tag = HashTag.objects.create(tag=hash_tag)
                    TagRelation.objects.create(hash_tag=tag, feed=feed)

        feedid = feed.id
        make_notification(7, feedid, request.user.id)
        return redirect('/feeds')

    elif request.user.is_anonymous:
        return redirect('/accounts/login')

    else:
        return render(request, 'feedpage/new.html')

def show(request, uuid):
    feed = Feed.objects.get(uuid=uuid)
    return render(request, 'feedpage/show.html', {'feed': feed})    

def delete(request, id):
    feed = Feed.objects.get(id=id)
    if request.is_ajax():
        if feed.creator == request.user:
            feed.delete()
            context = {}
        return JsonResponse(context)
    else:
        if feed.creator == request.user:
            feed.delete()
            next = '/feeds/'
        else:
            print("비정상적인 삭제 접근 시도")
            try:
                next = request.META['HTTP_REFERER']
            except:
                next = '/feeds/'
        return redirect('%s'%next)

def edit(request, uuid):
    feed = Feed.objects.get(uuid=uuid)
    if request.method == 'POST' and feed.creator == request.user and feed.feedcomment_set.count() == 0 and feed.upvote_set.count() == 0:
        title = request.POST['title']
        content_a = request.POST['content_a']
        content_b = request.POST['content_b']
        img_url_a = request.POST.get('img_url_a')
        img_url_b = request.POST.get('img_url_b')
        img_a = request.FILES.get('img_a')
        img_b = request.FILES.get('img_b')

        feed.title = title
        feed.content_a = content_a
        feed.content_b = content_b

        if img_a:
            feed.img_a = img_a
        if img_b:
            feed.img_b = img_b
        if img_url_a:
            name = urlparse(img_url_a).path.split('/')[-1]
            response = requests.get(img_url_a)
            if response.status_code == 200:
                feed.img_a.save(name, ContentFile(response.content), save=True)
        if img_url_b:
            name = urlparse(img_url_b).path.split('/')[-1]
            response = requests.get(img_url_b)
            if response.status_code == 200:
                feed.img_b.save(name, ContentFile(response.content), save=True)

        hash_tag_raw = request.POST['hash_tag_raw'].replace(" ", "")
        hash_tag_raw_edit = re.sub('[-=./?:$!@\|"^%*&()}{+]', '', hash_tag_raw)
        hash_tag_all = hash_tag_raw_edit.split("#")
        hash_tag_all = list(OrderedDict.fromkeys(hash_tag_all))

        for hash_tag in hash_tag_all:
            if hash_tag != "":
                if HashTag.objects.filter(tag=hash_tag).count() > 0:
                    tag = HashTag.objects.get(tag=hash_tag)
                    TagRelation.objects.create(hash_tag=tag, feed=feed)
                else:
                    tag = HashTag.objects.create(tag=hash_tag)
                    TagRelation.objects.create(hash_tag=tag, feed=feed)        #나중에는 태그 위치 조절할 수 있는 기능 / 특정 태그 삭제하는 기능 구현 필요

        feed.update_date()
        feed.save()
        next = request.POST['next']
        #여기로 보내기 위함=> '/feeds'+'?page='+feeds.number
        return redirect('%s'%next)
    elif request.user.is_anonymous:
        return redirect('/accounts/login')
    elif feed.creator == request.user and feed.feedcomment_set.count() == 0 and feed.upvote_set.count() == 0:
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return render(request, 'feedpage/edit.html', {'feed': feed, 'next': next})
    else:
        print("비정상적인 수정 접근 시도")
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)

def delete_tag(request, id, trid):
    print(trid)
    feed = Feed.objects.get(id=id)
    if feed.creator == request.user:
        if request.is_ajax():
            tag = TagRelation.objects.get(id=trid)
            tag.delete()
            context = {}
            return JsonResponse(context)
        else:
            tag = TagRelation.objects.get(id=trid)
            tag.delete()
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)


def create_comment(request, id):
    if request.method == 'POST':
        if request.is_ajax():
            upvote_list = Upvote.objects.filter(feed_id=id, user_id=request.user.id)
            if upvote_list.count() > 0:
                if upvote_list.first().about_a:
                    upvote_side = 1
                else:
                    upvote_side = 2
            else:
                upvote_side = 0
            content = request.POST['content']
            FeedComment.objects.create(feed_id=id, content=content, reactor=request.user, upvote_side=upvote_side)
            new_comment = FeedComment.objects.latest('id')
            context = {
                'comment': {
                    'id': new_comment.id,
                    'reactor': new_comment.reactor.username,
                    'content': new_comment.content,
                    'upvote_side': new_comment.upvote_side,
                }
            }
            make_notification(2, id, request.user.id)
            return JsonResponse(context)
        else:
            upvote_list = Upvote.objects.filter(feed_id=id, user_id=request.user.id)
            if upvote_list.count() > 0:
                if upvote_list.first().about_a:
                    upvote_side = 1
                else:
                    upvote_side = 2
            else:
                upvote_side = 0
            content = request.POST['content']
            FeedComment.objects.create(feed_id=id, content=content, reactor=request.user, upvote_side=upvote_side)
            make_notification(2, id, request.user.id)
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def delete_comment(request, id, cid):
    if request.is_ajax() and request.method == 'POST':
        context = {}
        c = FeedComment.objects.get(id=cid)
        c.delete()
        return JsonResponse(context)
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def upvote_comment(request, id, cid):
    # if request.method == 'POST':
    if request.is_ajax():
        c = FeedComment.objects.get(id=cid)
        upvote_list = c.commentupvote_set.filter(user_id = request.user.id)
        context = {}
        if upvote_list.count() > 0:
            c.commentupvote_set.get(user_id = request.user.id).delete()
            context['btn_name'] = 'favorite_border'
        else:
            CommentUpvote.objects.create(user_id = request.user.id, feedcomment_id = cid)
            context['btn_name'] = 'favorite'
            make_notification(5, cid, request.user.id)

        c.total_upvote = c.commentupvote_set.count()
        c.save()
        context['total_upvote'] = c.total_upvote
        return JsonResponse(context)
    else:
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)


#TODO: 리팩토링 필요하겠음
def feed_upvote_a(request, pk):
    feed = Feed.objects.get(id = pk)
    if request.is_ajax():
        upvote_list = feed.upvote_set.filter(user_id = request.user.id)
        upvote_total = feed.upvote_set.count() + 1
        upvote_a = feed.upvote_set.filter(about_a=True).count() + 1
        upvote_perc_a = "{:.0f}".format((upvote_a / upvote_total)*100)
        upvote_b = feed.upvote_set.filter(about_a=False).count()
        upvote_perc_b = "{:.0f}".format((upvote_b / upvote_total)*100)
        if upvote_list.count() > 0:
            Notification.objects.filter(feed=feed, noti_from=request.user.profile, noti_to=feed.creator.profile, noti_type=1).delete()
            if upvote_list.first().about_a:
                feed.upvote_set.filter(user_id = request.user.id).delete()
                upvote_a -= 2
                context = {
                    'upvote_after': 0,
                    'upvote_before': 1,
                    'upvote_a': upvote_a,
                    'perc_a': upvote_perc_a,
                    'upvote_b': upvote_b,
                    'perc_b': upvote_perc_b
                    }
            else:
                upvote_b -= 1
                upvote_total -= 1
                upvote_perc_a = "{:.0f}".format((upvote_a / upvote_total)*100)
                upvote_perc_b = "{:.0f}".format((upvote_b / upvote_total)*100)
                feed.upvote_set.filter(user_id = request.user.id).delete()
                Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
                context = {
                    'upvote_after': 1,
                    'upvote_before': 2,
                    'upvote_a': upvote_a,
                    'perc_a': upvote_perc_a,
                    'upvote_b': upvote_b,
                    'perc_b': upvote_perc_b
                    }
        else:
            Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
            # 노티 만들기
            make_notification(1, pk, request.user.id)
            context = {
                'upvote_after': 1,
                'upvote_before': 0,
                'upvote_a': upvote_a,
                'perc_a': upvote_perc_a,
                'upvote_b': upvote_b,
                'perc_b': upvote_perc_b
                }
        return JsonResponse(context)

    else:
        try:
            upvote_list = feed.upvote_set.filter(user_id = request.user.id)
            # feedcomment_list = feed.feedcomment_set.filter(reactor_id = request.user.id)
            if upvote_list.count() > 0:
                Notification.objects.filter(feed=feed, noti_from=request.user.profile, noti_to=feed.creator.profile, noti_type=1).delete()
                if upvote_list.first().about_a:
                    feed.upvote_set.filter(user_id = request.user.id).delete()
                else:
                    feed.upvote_set.filter(user_id = request.user.id).delete()
                    Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
            else:
                Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
                # 노티 만들기
                make_notification(1, pk, request.user.id)
            try:
                next = request.META['HTTP_REFERER']
            except:
                next = '/feeds/'
        except:
            next = '/accounts/login'
        return redirect('%s'%next)

def feed_upvote_b(request, pk):
    feed = Feed.objects.get(id = pk)
    if request.is_ajax():
        upvote_list = feed.upvote_set.filter(user_id = request.user.id)
        upvote_total = feed.upvote_set.count() + 1
        upvote_a = feed.upvote_set.filter(about_a=True).count()
        upvote_perc_a = "{:.0f}".format((upvote_a / upvote_total)*100)
        upvote_b = feed.upvote_set.filter(about_a=False).count() +1
        upvote_perc_b = "{:.0f}".format((upvote_b / upvote_total)*100)
        if upvote_list.count() > 0:
            Notification.objects.filter(feed=feed, noti_from=request.user.profile, noti_to=feed.creator.profile, noti_type=1).delete()
            if upvote_list.first().about_a:
                feed.upvote_set.filter(user_id = request.user.id).delete()
                upvote_a -= 1
                upvote_total -= 1
                upvote_perc_a = "{:.0f}".format((upvote_a / upvote_total)*100)
                upvote_perc_b = "{:.0f}".format((upvote_b / upvote_total)*100)
                Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
                context = {
                    'upvote_after': 2,
                    'upvote_before': 1,
                    'upvote_a': upvote_a,
                    'perc_a': upvote_perc_a,
                    'upvote_b': upvote_b,
                    'perc_b': upvote_perc_b
                    }
            else:
                feed.upvote_set.filter(user_id = request.user.id).delete()
                upvote_b -= 2
                context = {
                    'upvote_after': 0,
                    'upvote_before': 2,
                    'upvote_a': upvote_a,
                    'perc_a': upvote_perc_a,
                    'upvote_b': upvote_b,
                    'perc_b': upvote_perc_b
                    }
        else:
            Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
            # 노티 만들기
            make_notification(1, pk, request.user.id)
            context = {
                'upvote_after': 2,
                'upvote_before': 0,
                'upvote_a': upvote_a,
                'perc_a': upvote_perc_a,
                'upvote_b': upvote_b,
                'perc_b': upvote_perc_b
                }
        return JsonResponse(context)
    else:
        try:
            upvote_list = feed.upvote_set.filter(user_id = request.user.id)
            if upvote_list.count() > 0:
                Notification.objects.filter(feed=feed, noti_from=request.user.profile, noti_to=feed.creator.profile, noti_type=1).delete()
                if upvote_list.first().about_a: 
                    feed.upvote_set.filter(user_id = request.user.id).delete()
                    Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
                else:
                    feed.upvote_set.filter(user_id = request.user.id).delete()
            else:
                Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
                # 노티 만들기
                make_notification(1, pk, request.user.id)
            try:
                next = request.META['HTTP_REFERER']
            except:
                next = '/feeds/'
        except:
            next = '/accounts/login'
        return redirect('%s'%next)

def follow_manager(request, pk):
    if request.is_ajax():
        follow_from = request.user.profile
        follow_to = Profile.objects.get(user_id = pk)
        print(follow_from)
        print(follow_to)
        following_already = Follow.objects.filter(follow_from=follow_from, follow_to=follow_to)
        print(following_already.count())
        if following_already.count() > 0:
            following_already.first().delete()
            context = {'message': '구독하기'}
        else:
            Follow.objects.create(follow_from=follow_from, follow_to=follow_to)
            context = {'message': '구독취소'}
            # 노티 만들기
            make_notification(6, pk, request.user.id)
        return JsonResponse(context)
    else:
        follow_from = request.user.profile
        follow_to = Profile.objects.get(user_id = pk)
        following_already = Follow.objects.filter(follow_from=follow_from, follow_to=follow_to)
        if following_already.count() > 0:
            following_already.first().delete()
        else:
            Follow.objects.create(follow_from=follow_from, follow_to=follow_to)
            # 노티 만들기
            make_notification(6, pk, request.user.id)
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)

def report(request, pk):
    feed = Feed.objects.get(id = pk)
    report_count_mine = feed.report_set.filter(user_id = request.user.id).count()
    report_count = Report.objects.filter(feed_id = feed.id).count()
    if request.is_ajax():
        if report_count_mine == 0:
            Report.objects.create(user_id = request.user.id, feed_id = feed.id)
            context = {'total_report': report_count+1, 'report_before': 0}
            # 노티 만들기
            if report_count > 9:
                make_notification(4, pk, request.user.id)
            else:
                make_notification(3, pk, request.user.id)
        else: 
            context = {'total_report': report_count, 'report_before': 1}
        return JsonResponse(context)

    else:
        if report_count_mine == 0:
            Report.objects.create(user_id = request.user.id, feed_id = feed.id)
            # 노티 만들기
            if report_count > 9:
                make_notification(4, pk, request.user.id)
            else:
                make_notification(3, pk, request.user.id)
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)

def statistics(request, pk, stat_menu, stat_name):
    if request.is_ajax():
        count_a, count_b = 0, 0
        upvote_a = Upvote.objects.filter(feed_id = pk, about_a = True)
        upvote_b = Upvote.objects.filter(feed_id = pk, about_a = False)
        if stat_name == '남성':
            count_a = upvote_a.filter(user__profile__is_male = True).count()
            count_b = upvote_b.filter(user__profile__is_male = True).count()
        elif stat_name == '여성':
            count_a = upvote_a.filter(user__profile__is_male = False).count()
            count_b = upvote_b.filter(user__profile__is_male = False).count()
        elif stat_name == '10대미만':
            count_a = upvote_a.filter(user__profile__birth__gte = 2010).count()
            count_b = upvote_b.filter(user__profile__birth__gte = 2010).count()
        elif stat_name == '10대':
            count_a = upvote_a.filter(user__profile__birth__gte = 2000, user__profile__birth__lte = 2009).count()
            count_b = upvote_b.filter(user__profile__birth__gte = 2000, user__profile__birth__lte = 2009).count()
        elif stat_name == '20대':
            count_a = upvote_a.filter(user__profile__birth__gte = 1990, user__profile__birth__lte = 1999).count()
            count_b = upvote_b.filter(user__profile__birth__gte = 1990, user__profile__birth__lte = 1999).count()
        elif stat_name == '30대':
            count_a = upvote_a.filter(user__profile__birth__gte = 1980, user__profile__birth__lte = 1989).count()
            count_b = upvote_b.filter(user__profile__birth__gte = 1980, user__profile__birth__lte = 1989).count()
        elif stat_name == '40대':
            count_a = upvote_a.filter(user__profile__birth__gte = 1970, user__profile__birth__lte = 1979).count()
            count_b = upvote_b.filter(user__profile__birth__gte = 1970, user__profile__birth__lte = 1979).count()
        elif stat_name == '50대이상':
            count_a = upvote_a.filter(user__profile__birth__lte = 1969).count()
            count_b = upvote_b.filter(user__profile__birth__lte = 1969).count()
        elif stat_name == 'iOS':
            count_a = upvote_a.filter(user__profile__likes_iphone = True).count()
            count_b = upvote_b.filter(user__profile__likes_iphone = True).count()
        elif stat_name == 'Android':
            count_a = upvote_a.filter(user__profile__likes_iphone = False).count()
            count_b = upvote_b.filter(user__profile__likes_iphone = False).count()
        elif stat_name == '서울경기':
            count_a = upvote_a.filter(user__profile__region = 1).count()
            count_b = upvote_b.filter(user__profile__region = 1).count()
        elif stat_name == '강원':
            count_a = upvote_a.filter(user__profile__region = 2).count()
            count_b = upvote_b.filter(user__profile__region = 2).count()
        elif stat_name == '충청':
            count_a = upvote_a.filter(user__profile__region = 3).count()
            count_b = upvote_b.filter(user__profile__region = 3).count()
        elif stat_name == '호남':
            count_a = upvote_a.filter(user__profile__region = 4).count()
            count_b = upvote_b.filter(user__profile__region = 4).count()
        elif stat_name == '영남':
            count_a = upvote_a.filter(user__profile__region = 5).count()
            count_b = upvote_b.filter(user__profile__region = 5).count()
        elif stat_name == '제주':
            count_a = upvote_a.filter(user__profile__region = 6).count()
            count_b = upvote_b.filter(user__profile__region = 6).count()
        elif stat_name == '국내전체':
            count_a = upvote_a.filter(user__profile__region__lte = 6).count()
            count_b = upvote_b.filter(user__profile__region__lte = 6).count()
        elif stat_name == '해외':
            count_a = upvote_a.filter(user__profile__region = 7).count()
            count_b = upvote_b.filter(user__profile__region = 7).count()
        elif stat_name == '기타' and stat_menu == 'region':
            count_a = upvote_a.filter(user__profile__region = 8).count()
            count_b = upvote_b.filter(user__profile__region = 8).count()
        elif stat_name == '진보':
            count_a = upvote_a.filter(user__profile__left_level = 5).count()
            count_b = upvote_b.filter(user__profile__left_level = 5).count()
        elif stat_name == '중도진보':
            count_a = upvote_a.filter(user__profile__left_level = 4).count()
            count_b = upvote_b.filter(user__profile__left_level = 4).count()
        elif stat_name == '중도':
            count_a = upvote_a.filter(user__profile__left_level = 3).count()
            count_b = upvote_b.filter(user__profile__left_level = 3).count()
        elif stat_name == '중도보수':
            count_a = upvote_a.filter(user__profile__left_level = 2).count()
            count_b = upvote_b.filter(user__profile__left_level = 2).count()
        elif stat_name == '보수':
            count_a = upvote_a.filter(user__profile__left_level = 1).count()
            count_b = upvote_b.filter(user__profile__left_level = 1).count()
        elif stat_name == '무교':
            count_a = upvote_a.filter(user__profile__religion = 4).count()
            count_b = upvote_b.filter(user__profile__religion = 4).count()
        elif stat_name == '기독교계열':
            count_a = upvote_a.filter(user__profile__religion = 3).count()
            count_b = upvote_b.filter(user__profile__religion = 3).count()
        elif stat_name == '불교계열':
            count_a = upvote_a.filter(user__profile__religion = 2).count()
            count_b = upvote_b.filter(user__profile__religion = 2).count()
        elif stat_name == '기타' and stat_menu == 'religion':
            count_a = upvote_a.filter(user__profile__religion = 1).count()
            count_b = upvote_b.filter(user__profile__religion = 1).count()
        elif stat_name == '문과계열':
            count_a = upvote_a.filter(user__profile__major = "문과").count()
            count_b = upvote_b.filter(user__profile__major = "문과").count()
        elif stat_name == '이과계열':
            count_a = upvote_a.filter(user__profile__major = "이과").count()
            count_b = upvote_b.filter(user__profile__major = "이과").count()
        elif stat_name == '예체능계열':
            count_a = upvote_a.filter(user__profile__major = "예체능").count()
            count_b = upvote_b.filter(user__profile__major = "예체능").count()
        elif stat_name == '기타' and stat_menu == '전공분야':
            count_a = upvote_a.filter(user__profile__major = "기타").count()
            count_b = upvote_b.filter(user__profile__major = "기타").count()

        context = {
            'count_a': count_a,
            'count_b': count_b
        }
        return JsonResponse(context)
    else:
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)

def creator(request, creator_name):
    creators = User.objects.filter(username=creator_name)
    if creators.count() > 0:
        creator = creators.first()
        feeds = Feed.objects.filter(creator=creator).order_by('-updated_at', '-created_at')
        if len(feeds) == 0:
            has_feeds = False
        else:
            has_feeds = True
        return render(request, 'feedpage/creator.html', {'has_feeds': has_feeds, 'feeds': feeds, 'creator': creator})
    else:
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)

def mysubscribe(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    follow_from = request.user.profile
    my_subs = Follow.objects.filter(follow_from=follow_from)
    feeds = []
    for my_sub in my_subs:
        my_sub_user = my_sub.follow_to.user
        feeds = feeds + list(my_sub_user.feed_set.all())
    feeds = sorted(feeds , key = lambda x: x.updated_at, reverse=True)

    has_subs, has_feeds = False, False

    if len(my_subs) == 0:
        has_subs = False
    else:
        has_subs = True
        if len(feeds) == 0:
            has_feeds = False
        else:
            has_feeds = True

    return render(request, 'feedpage/mysubscribe.html', {'feeds': feeds, 'my_subs': my_subs, 'has_subs': has_subs, 'has_feeds': has_feeds})

def myupload(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    feeds = Feed.objects.filter(creator_id=request.user.id).order_by('-updated_at', '-created_at')
    return render(request, 'feedpage/myupload.html', {'feeds': feeds})

def myreaction(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    upvotes = request.user.upvote_set.exclude(feed__creator = request.user).order_by('-created_at')
    if len(upvotes) == 0:
        has_upvotes = False
    else:
        has_upvotes = True
    return render(request, 'feedpage/myreaction.html', {'upvotes': upvotes, 'has_upvotes': has_upvotes})

def mynotification(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    noti = Notification.objects.filter(noti_to=request.user.profile, is_mine=False).order_by('-created_at')
    noti_unchecked = noti.filter(is_checked=False) #지난번기준 미확인알림
    profile = request.user.profile
    
    for each_noti in noti_unchecked:
        if each_noti.created_at < profile.notichecked_at:
            each_noti.is_checked = True
            each_noti.save()

    noti_unchecked = noti.filter(is_checked=False) #새로운기준 확인알림
    noti_checked = noti.filter(is_checked=True)

    profile.notichecked_at = timezone.now()
    profile.save()

    has_noti = False

    if len(noti) == 0:
        has_noti = False
    else:
        has_noti = True

    return render(request, 'feedpage/mynotification.html', {'has_noti':has_noti, 'noti': noti, 'noti_unchecked': noti_unchecked, 'noti_checked': noti_checked})

#이미지 추천기능
def image_search(request):
    CLIENT_ID = IMG_CLIENT_ID
    CLIENT_SECRET = IMG_CLIENT_KEY
    DISPLAY_NUM = "40"
    text = request.POST['keyword']

    enc_text = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/image?display="+ DISPLAY_NUM +"&query=" + enc_text

    image_search_request = urllib.request.Request(url)
    image_search_request.add_header('X-Naver-Client-Id', CLIENT_ID)
    image_search_request.add_header('X-Naver-Client-Secret', CLIENT_SECRET)
    response = urllib.request.urlopen(image_search_request)

    if response.getcode() == 200:
        image_response = response.read().decode('utf-8')
        image_response = json.loads(image_response)
        context = {
            'result': image_response
        }
    else:
    	print('Error Code: ' + response.getcode())

    return JsonResponse(context)
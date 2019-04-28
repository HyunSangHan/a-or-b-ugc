from django.shortcuts import render
from .models import Feed, FeedComment, Upvote #(참고: .models == feeds.models)
from accounts.models import Profile, Follow
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User 

def index(request): 
    if request.method == 'POST': # create
        title = request.POST['title']
        content_a = request.POST['content_a']
        content_b = request.POST['content_b']
        Feed.objects.create(title=title, content_a=content_a, content_b=content_b, creator = request.user)

        return redirect('/feeds')
    else: # index
        keyword = request.GET.get('keyword', '')
        feeds_all = Feed.objects.all().order_by('-updated_at', '-created_at')
        if keyword: 
            feeds_all = feeds_all.filter(Q(title__icontains=keyword) | Q(content_a__icontains=keyword) | Q(content_b__icontains=keyword))
        paginator = Paginator(feeds_all, 8)
        page_num = request.GET.get('page')
        feeds = paginator.get_page(page_num)
        search_result_num = len(feeds_all)
        # print(type(feeds_all.get(id=38).get_percentage()))
        if keyword and feeds:
            is_searched = True
        elif keyword == '':
            is_searched = False
        else:
            is_searched = True
        return render(request, 'feedpage/index.html', {'feeds': feeds, 'keyword': keyword, 'page': page_num, 'is_searched': is_searched, 'search_result_num': search_result_num})
#문제1: page1일때 next 파라미터를 못넘김
#문제2: page2부터는 next 파라미터를 잘 넘기는데도 활용되지 못하고 있음

def new(request):
    feed = Feed()
    return render(request, 'feedpage/new.html', {'feed': feed})

def show(request, id):
    feed = Feed.objects.get(id=id)
    return render(request, 'feedpage/show.html', {'feed': feed})    

def delete(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect('/feeds')

def edit(request, id):
    feed = Feed.objects.get(id=id)
    if request.method == 'POST':
        feed.title = request.POST['title']
        feed.content_a = request.POST['content_a']
        feed.content_b = request.POST['content_b']
        feed.editnow = False
        feed.save()
        #여기로 보내고 싶은데... '/feeds'+'?page='+feeds.number
        return redirect('/feeds')
    else:
        return render(request, 'feedpage/edit.html', {'feed': feed})    

def editon(request, id):
    feed = Feed.objects.get(id=id)
    feed.editnow = True
    feed.save()
    return redirect(request.META['HTTP_REFERER'])

def editoff(request, id):
    feed = Feed.objects.get(id=id)
    feed.editnow = False
    feed.save()
    return redirect(request.META['HTTP_REFERER'])

def create_comment(request, id):
    content = request.POST['content']
    about_a = request.POST['about_a']
    FeedComment.objects.create(feed_id=id, content=content, about_a=about_a, reactor=request.user)
    return redirect(request.META['HTTP_REFERER'])

def delete_comment(request, id, cid):
    c = FeedComment.objects.get(id=cid)
    c.delete()
    return redirect(request.META['HTTP_REFERER'])


# 리팩토링 필요하겠음
def feed_upvote_a(request, pk):
    # feed id로 한번 필터링하고(정확히는, 불러오고)
    feed = Feed.objects.get(id = pk)
    # user id로 한번 더 필터링하고
    upvote_list = feed.upvote_set.filter(user_id = request.user.id)
    if upvote_list.count() > 0:
        if upvote_list.first().about_a: 
            feed.upvote_set.get(user_id = request.user.id).delete()
        else:
            feed.upvote_set.get(user_id = request.user.id).delete()
            Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
    else:
        Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
    return redirect(request.META['HTTP_REFERER'])

def feed_upvote_b(request, pk):
    # feed id로 한번 필터링하고(정확히는, 불러오고)
    feed = Feed.objects.get(id = pk)
    # user id로 한번 더 필터링하고
    upvote_list = feed.upvote_set.filter(user_id = request.user.id)
    if upvote_list.count() > 0:
        if upvote_list.first().about_a: 
            feed.upvote_set.get(user_id = request.user.id).delete()
            Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
        else:
            feed.upvote_set.get(user_id = request.user.id).delete()
    else:
        Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
    return redirect(request.META['HTTP_REFERER'])

def follow_manager(request, pk):
    follow_from = Profile.objects.get(user_id = request.user.id)
    follow_to = Profile.objects.get(user_id = pk)

    try:
        following_already = Follow.objects.get(follow_from=follow_from, follow_to=follow_to)
    except Follow.DoesNotExist:
        following_already = None

    if following_already:
        following_already.delete()
    else:
        # Follow.objects.create(follow_from=follow_from, follow_to=follow_to)
        f = Follow()
        f.follow_from, f.follow_to = follow_from, follow_to
        f.save()

    return redirect(request.META['HTTP_REFERER'])
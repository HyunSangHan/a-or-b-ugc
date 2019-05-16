from django.shortcuts import render
from .models import Feed, FeedComment, HashTag, TagRelation, Upvote, CommentUpvote, Report #(참고: .models == feeds.models)
from accounts.models import Profile, Follow
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

###니드 로그인 기능 리다이렉트 구현 필요

def index(request): 
    # print(HashTag.objects.all())
    keyword = request.GET.get('keyword', '')
    feeds_all = Feed.objects.all().order_by('-updated_at', '-created_at')
#검색기능 추후 보완 필요
    if keyword: 
        #필드에서 피드 뽑아오기
        feeds_by_field = list(feeds_all.filter(Q(title__icontains=keyword) | Q(content_a__icontains=keyword) | Q(content_b__icontains=keyword)))
        #해시태그에서 피드 뽑아오기
        feeds_by_hashtag = []
        tags = HashTag.objects.all().filter(Q(tag__icontains=keyword))
        for tag in tags:
            feeds_by_hashtag = feeds_by_hashtag + list(tag.tagged_feeds.all())
        feeds_all = list(set(feeds_by_field + feeds_by_hashtag))
#페이지네이션과의 파라미터 조화 필요

    paginator = Paginator(feeds_all, 8)
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

def new(request):
    if request.method == 'POST': # create
        title = request.POST['title']
        content_a = request.POST['content_a']
        content_b = request.POST['content_b']
        img_a = request.FILES.get('img_a', False)
        img_b = request.FILES.get('img_b', False)
        feed = Feed.objects.create(title=title, content_a=content_a, img_a=img_a, img_b=img_b, content_b=content_b, creator = request.user)
        #edit도
        # 띄어쓰기 포함도
        # 샾 안넣었을때의 코너케이스도 챙기기 필요
        # replace왜 안먹히지? 확인 필요
        hash_tag_raw = request.POST['hash_tag_raw'].replace(" ", "")
        hash_tag_all = hash_tag_raw.split("#")
        for hash_tag in hash_tag_all:
            ###################################
            if HashTag.objects.filter(tag=hash_tag).count() > 0:
                tag = HashTag.objects.get(tag=hash_tag)
                TagRelation.objects.create(hash_tag=tag, feed=feed)
            else:
                tag = HashTag.objects.create(tag=hash_tag)
                TagRelation.objects.create(hash_tag=tag, feed=feed)
# 공백이면 빼는 로직도 필요(당장 / below)
# 왜 이거 안됨? => [에러메시지] invalid literal for int() with base 10: ''
# print(TagRelation.objects.filter(hash_tag="").count())
# TagRelation.objects.get(hash_tag="").delete()
        return redirect('/feeds')
    else:
        return render(request, 'feedpage/new.html')

def show(request, id):
    feed = Feed.objects.get(id=id)
    return render(request, 'feedpage/show.html', {'feed': feed})    

def delete(request, id):
    print(request.method)
    if request.method == "POST":
        feed = Feed.objects.get(id=id)
        feed.delete()
        return redirect('/feeds')
    else:
        return redirect('/feeds')

def edit(request, id):
    feed = Feed.objects.get(id=id)
    if request.method == 'POST' and feed.creator == request.user and feed.feedcomment_set.count() == 0 and feed.upvote_set.count() == 0:
        feed.title = request.POST['title']
        feed.content_a = request.POST['content_a']
        feed.content_b = request.POST['content_b']
        hash_tag_raw = request.POST['hash_tag_raw']
        hash_tag_all = hash_tag_raw.split("#")
        for hash_tag in hash_tag_all:
            if HashTag.objects.filter(tag=hash_tag).count() > 0:
                tag = HashTag.objects.get(tag=hash_tag)
                if TagRelation.objects.filter(hash_tag=tag, feed=feed).count() == 0:
                    TagRelation.objects.create(hash_tag=tag, feed=feed)
            else:
                tag = HashTag.objects.create(tag=hash_tag)
                TagRelation.objects.create(hash_tag=tag, feed=feed)
        #현재상황: edit을 통해 추가된 태그의 첫번째는 #만이 나오는 게 그대로 나오고 있음. 해시태그 하나씩 삭제가 안됨.(form태그 중첩 이슈로 예상)
        #나중에는 태그 위치 조절할 수 있는 기능 / 특정 태그 삭제하는 기능 구현 필요

        feed.editnow = False
        feed.update_date()
        feed.save()
        next = request.POST['next']
        #여기로 보내기 위함=> '/feeds'+'?page='+feeds.number
        return redirect('%s'%next)
    elif feed.creator == request.user and feed.feedcomment_set.count() == 0 and feed.upvote_set.count() == 0:
        next = request.META['HTTP_REFERER']
        return render(request, 'feedpage/edit.html', {'feed': feed, 'next': next})
    else:
        print("비정상적인 수정 접근 시도")
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)

def delete_tag(request, fid, tid):
    #되고 있는 것인지 확인 필요
    ####################################
    if request.method == 'DELETE':
        tag = HashTag.objects.get(feed_id=fid, tag_id=tid)
        tag.delete()
        return redirect(request.META['HTTP_REFERER'])

def create_comment(request, id):
    if request.method == 'POST':
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
        print(FeedComment.objects.filter(feed_id=id, reactor=request.user).first().upvote_side)
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def delete_comment(request, id, cid):
    if request.method == 'POST':
        c = FeedComment.objects.get(id=cid)
        c.delete()
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def upvote_comment(request, id, cid):
    if request.method == 'POST':
        c = FeedComment.objects.get(id=cid)
        upvote_list = c.commentupvote_set.filter(user_id = request.user.id)
        if upvote_list.count() > 0:
            c.commentupvote_set.get(user_id = request.user.id).delete()
        else:
            CommentUpvote.objects.create(user_id = request.user.id, feedcomment_id = cid)
        c.total_upvote = c.commentupvote_set.count()
        c.save()
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

# 리팩토링 필요하겠음
def feed_upvote_a(request, pk):
    # if request.method == 'POST':
    # 포스트로 안날려도 되나????????

    # feed id로 한번 필터링하고(정확히는, 불러오고)
    feed = Feed.objects.get(id = pk)
    # user id로 한번 더 필터링하고
    upvote_list = feed.upvote_set.filter(user_id = request.user.id)
    feedcomment_list = feed.feedcomment_set.filter(reactor_id = request.user.id)
    if upvote_list.count() > 0:
        if upvote_list.first().about_a:
            feed.upvote_set.get(user_id = request.user.id).delete()
        else:
            feed.upvote_set.get(user_id = request.user.id).delete()
            Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
    else:
        Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = True)
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def feed_upvote_b(request, pk):
    # if request.method == 'POST':
    feed = Feed.objects.get(id = pk)
    upvote_list = feed.upvote_set.filter(user_id = request.user.id)
    feedcomment_list = feed.feedcomment_set.filter(reactor_id = request.user.id)
    if upvote_list.count() > 0:
        if upvote_list.first().about_a: 
            feed.upvote_set.get(user_id = request.user.id).delete()
            Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
        else:
            feed.upvote_set.get(user_id = request.user.id).delete()
    else:
        Upvote.objects.create(user_id = request.user.id, feed_id = feed.id, about_a = False)
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def follow_manager(request, pk):
    if request.method == 'POST':
        follow_from = Profile.objects.get(user_id = request.user.id)
        follow_to = Profile.objects.get(user_id = pk)
        try:
            following_already = Follow.objects.get(follow_from=follow_from, follow_to=follow_to)
        except Follow.DoesNotExist:
            #갑자기 이거뭐지???????????????????
            following_already = None

        if following_already:
            following_already.delete()
        else:
            # Follow.objects.create(follow_from=follow_from, follow_to=follow_to)
            f = Follow()
            f.follow_from, f.follow_to = follow_from, follow_to
            f.save()

    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def report(request, pk):
    # if request.method == 'POST':    
    feed = Feed.objects.get(id = pk)
    report_count = feed.report_set.filter(user_id = request.user.id).count()
    if report_count == 0:
        Report.objects.create(user_id = request.user.id, feed_id = feed.id)
    try:
        next = request.META['HTTP_REFERER']
    except:
        next = '/feeds/'
    return redirect('%s'%next)

def statistics(request, id):
    if request.method == "POST":
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)
    else:
        return render(request, 'feedpage/statistics.html', {'test': 'test'})

def creator(request, creator_name):
    print("================="+creator_name)
    creators = User.objects.filter(username=creator_name)
    if creators.count() > 0:
        creator = creators.first()
        feeds = Feed.objects.filter(creator=creator)
        print(feeds)
        return render(request, 'feedpage/creator.html', {'feeds': feeds})
    else:
        try:
            next = request.META['HTTP_REFERER']
        except:
            next = '/feeds/'
        return redirect('%s'%next)

def mysubscribe(request):
    # my_subs = Follow.objects.()
    # 이거 아님!
    feeds = Feed.objects.filter(creator_id=request.user.id)
    print(feeds)
    return render(request, 'feedpage/mysubscribe.html', {'feeds': feeds})

def myhistory(request):
    feeds = Feed.objects.filter(creator_id=request.user.id)
    print(feeds)
    return render(request, 'feedpage/myhistory.html', {'feeds': feeds})

def myreaction(request):
    feeds = Feed.objects.filter(creator_id=request.user.id)
    print(feeds)
    return render(request, 'feedpage/myreaction.html', {'feeds': feeds})
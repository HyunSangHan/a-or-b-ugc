from django import template
from feedpage.models import Feed, FeedComment, Upvote, HashTag, TagRelation, Report, Notification
register = template.Library()
from datetime import datetime, timedelta
from django.utils import timezone

@register.simple_tag
def get_deltatime(pk, type_id):
    nowtime = timezone.now()
    if type_id == 1: #피드일때
        feedtime = Feed.objects.get(id=pk).updated_at
        deltatime = nowtime-feedtime
    if type_id == 2: #알림일때
        notitime = Notification.objects.get(id=pk).created_at
        deltatime = nowtime-notitime
    delta_second = deltatime.seconds
    delta_day = deltatime.days

    if delta_day == 0:
        if delta_second < 10:
            deltatime_view = "방금전"
        elif delta_second < 60:
            deltatime_view = str(delta_second) + "초전"
        elif delta_second < 3600:
            delta_minute = deltatime.seconds // 60
            deltatime_view = str(delta_minute) + "분전"
        else: # delta_second >= 3600
            delta_hour = deltatime.seconds // 3600
            deltatime_view = str(delta_hour) + "시간전"
    else: # delta_day > 0
        if delta_day < 30:
            deltatime_view = str(delta_day) + "일전"
        elif delta_day < 365:
            delta_month = deltatime.days // 30
            dletatime_view = str(delta_month) + "개월전"
        else: #delta_day >= 365
            delta_year = deltatime.days // 365
            dletatime_view = str(delta_year) + "일전"
    return deltatime_view

@register.simple_tag
def get_upvote_a(pk):
    feed = Feed.objects.get(id=pk)
    upvote_a = feed.upvote_set.filter(about_a=True).count()
    return upvote_a

@register.simple_tag
def get_upvote_b(pk):
    feed = Feed.objects.get(id=pk)
    upvote_b = feed.upvote_set.filter(about_a=False).count()
    return upvote_b

@register.simple_tag
def get_upvote_perc_a(pk):
    feed = Feed.objects.get(id=pk)
    upvote_total = feed.upvote_set.count()
    if upvote_total > 0:
        upvote_a = feed.upvote_set.filter(about_a=True).count()
        upvote_perc_a = "{:.0f}".format((upvote_a / upvote_total)*100)
    else: 
        upvote_perc_a = "-"
    return upvote_perc_a

@register.simple_tag
def get_upvote_perc_b(pk):
    feed = Feed.objects.get(id=pk)
    upvote_total = feed.upvote_set.count()
    if upvote_total > 0:
        upvote_b = feed.upvote_set.filter(about_a=False).count()
        upvote_perc_b = "{:.0f}".format((upvote_b / upvote_total)*100)
    else: 
        upvote_perc_b = "-"
    return upvote_perc_b
    
@register.simple_tag
def get_side(fid, cid):
    feed = Feed.objects.get(id=fid)
    feedcomment = feed.feedcomment_set.get(id=cid)
    if feedcomment.upvote_side == 1:
        side = "A"
    elif feedcomment.upvote_side == 2:
        side = "B"
    else:
        side = ""
    return side

# 지금은 유효하지 않음
@register.simple_tag
def get_upvote_color(fid, uid):
    feed = Feed.objects.get(id=fid)
    try:
        side_tf = feed.upvote_set.get(user_id = uid).about_a
        if side_tf:
            side = "A"
        else:
            side = "B"
    except:
        side = ""
    return side

@register.simple_tag
def get_report_tf(fid, uid):
    if Report.objects.filter(feed_id=fid, user_id=uid).count() != 0:
        report_tf = True
    else:
        report_tf = False
    return report_tf

@register.simple_tag
def get_feed_tags(fid):
    try:
        feed_tags_all = TagRelation.objects.filter(feed_id=fid)
    except:
        feed_tags_all = None

    # 태그노출 중복 제거를 위한 코드
    # '일단은' 구현했으나, 더 개선된 로직으로 수정 필요
    feed_tags = []
    for feed_tag in feed_tags_all:
        if feed_tag != feed_tags_all.first():
            feed_tags.append(str(feed_tag))
    return list(set(feed_tags))

@register.simple_tag
def get_comment_upvote_tf(fid, cid, uid):
    feed = Feed.objects.get(id=fid)
    comment = feed.feedcomment_set.get(id=cid)
    if comment.commentupvote_set.filter(user_id=uid).count() > 0:
        comment_upvote_tf = True
    else:
        comment_upvote_tf = False
    return comment_upvote_tf

# A에 대한 best댓글을 뽑아내기(index용)
@register.simple_tag
def get_bestcomment_a(fid):
    feed = Feed.objects.get(id=fid)
    comments_a_all = feed.feedcomment_set.filter(upvote_side=1)
    comments = comments_a_all.order_by('-total_upvote', 'created_at')
    comment_a = comments.first()
    if comment_a is not None:
        if comment_a.total_upvote > 0:
            return comment_a
    return

# B에 대한 best댓글을 뽑아내기(index용)
@register.simple_tag
def get_bestcomment_b(fid):
    feed = Feed.objects.get(id=fid)
    comments_b_all = feed.feedcomment_set.filter(upvote_side=2)
    comments = comments_b_all.order_by('-total_upvote', 'created_at')
    comment_b = comments.first()
    if comment_b is not None:
        if comment_b.total_upvote > 0:
            return comment_b
    return

# best댓글 제외한 댓글 전체 다 뽑아내기(index용)
@register.simple_tag
def get_ordered_comment_rest(fid, is_index):
    feed = Feed.objects.get(id=fid)
    a_is_best = feed.feedcomment_set.filter(upvote_side=1).exclude(total_upvote=0).count()
    b_is_best = feed.feedcomment_set.filter(upvote_side=2).exclude(total_upvote=0).count()
    comments_a, comments_b = [], []
    if a_is_best > 0 and b_is_best > 0:
        comments_a = list(feed.feedcomment_set.filter(upvote_side=1).order_by('-total_upvote', 'created_at')[1:])
        comments_b = list(feed.feedcomment_set.filter(upvote_side=2).order_by('-total_upvote', 'created_at')[1:])
    else:
        comments_a = list(feed.feedcomment_set.filter(upvote_side=1).order_by('-total_upvote', 'created_at'))
        comments_b = list(feed.feedcomment_set.filter(upvote_side=2).order_by('-total_upvote', 'created_at'))
    comments_etc = list(feed.feedcomment_set.filter(upvote_side=0))
    comments_all = comments_a + comments_b + comments_etc
    comments_all = sorted(comments_all, key=lambda x: x.created_at, reverse=True)
    if is_index:
        comments_all = sorted(comments_all, key=lambda x: x.total_upvote, reverse=True)
    comments = comments_all

    return comments

# 내 댓글만 뽑아내기(index용)
@register.simple_tag
def get_my_comment(fid, uid):
    feed = Feed.objects.get(id=fid)
    comments_all = feed.feedcomment_set.filter(reactor_id = uid)
    #댓글 랭킹로직: [1순위] 좋아요 많이받은순 / [2순위] 오래된순. 나중에는 각자 선택할 수 있게끔 구현 필요
    comments = comments_all.order_by('-total_upvote', 'created_at')
    return comments

# 댓글 전체 다 뽑아내기(show용)
@register.simple_tag
def get_ordered_comment(fid):
    feed = Feed.objects.get(id=fid)
    comments_all = feed.feedcomment_set
    #댓글 랭킹로직: [1순위] 좋아요 많이받은순 / [2순위] 오래된순. 나중에는 각자 선택할 수 있게끔 구현 필요
    comments = comments_all.order_by('-total_upvote', 'created_at')
    return comments

# 좋아요나 댓글 달린 경우 글을 수정하지 못하게 하는 판별용
@register.simple_tag
def is_deletable(fid):
    feed = Feed.objects.get(id=fid)
    if feed.feedcomment_set.count() > 0 or feed.upvote_set.count() > 0:
        deletable = False
    else:
        deletable = True
    return deletable

@register.simple_tag
def get_noti_amount(uid):
    noti = Notification.objects.filter(noti_to=uid, is_mine=False)
    noti_unchecked = noti.filter(is_checked=False) #지난번기준 미확인알림
    noti_amount_unchecked = noti_unchecked.count()
    return noti_amount_unchecked
from django import template
from feedpage.models import Feed, FeedComment, Upvote, HashTag, TagRelation, Report
register = template.Library()

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
        upvote_perc_a = "{:.1%}".format(upvote_a / upvote_total)
    else: 
        upvote_perc_a = "-"
    return upvote_perc_a

@register.simple_tag
def get_upvote_perc_b(pk):
    feed = Feed.objects.get(id=pk)
    upvote_total = feed.upvote_set.count()
    if upvote_total > 0:
        upvote_b = feed.upvote_set.filter(about_a=False).count()
        upvote_perc_b = "{:.1%}".format(upvote_b / upvote_total)
    else: 
        upvote_perc_b = "-"
    return upvote_perc_b
    
@register.simple_tag
def get_side(fid, cid):
    feed = Feed.objects.get(id=fid)
    comment = feed.feedcomment_set.get(id=cid)
    reactor = comment.reactor
    try:
        side_tf = feed.upvote_set.get(user = reactor).about_a
        if side_tf:
            side = "[A] "
        else:
            side = "[B] "
    except:
        side = ""
    return side

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

@register.simple_tag
def get_ordered_comment(fid, cid, uid):
    feed = Feed.objects.get(id=fid)
    comments_all = feed.feedcomment_set
    #댓글 랭킹로직: [1순위] 좋아요 많이받은순 / [2순위] 오래된순. 나중에는 각자 선택할 수 있게끔 구현 필요
    comments = comments_all.order_by('-total_upvote', 'created_at')
    return comments
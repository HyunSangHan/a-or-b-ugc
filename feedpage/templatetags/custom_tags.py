from django import template
from feedpage.models import Feed, FeedComment, Upvote, HashTag, Report
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

############여기해결하는중
@register.simple_tag
def get_report_tf(fid, uid):
    if Report.objects.filter(feed_id=fid, user_id=uid).count() != 0:
        report_tf = True
    else:
        report_tf = False
    return report_tf
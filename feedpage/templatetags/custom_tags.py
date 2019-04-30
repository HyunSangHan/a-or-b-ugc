from django import template
from feedpage.models import Feed, FeedComment, Upvote, HashTag
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
def get_hashtag_set(pk):
    feed = Feed.objects.get(id=pk)
    hashtag_total = feed.hashtag_set.all()
    return hashtag_total
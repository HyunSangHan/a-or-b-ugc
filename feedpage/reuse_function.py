from django.shortcuts import render
from .models import Feed, FeedComment, HashTag, TagRelation, Upvote, CommentUpvote, Report, Notification
from accounts.models import Profile, Follow
from django.contrib.auth.models import User

def make_notification(noti_type, fid, uid):
# tid Cases => 1피드투표/2피드댓글/3신고/4신고숨김/5댓글좋아요/6구독/7구독새글
    if noti_type == 1 or noti_type == 2: #피드투표 or 피드댓글
        feed = Feed.objects.get(id=fid)
        noti_from = Profile.objects.get(user_id = uid)
        noti_to = Profile.objects.get(user = feed.creator)
        if noti_from != noti_to:
            is_mine = False
        else:
            is_mine = True
        Notification.objects.create(feed=feed, noti_from=noti_from, noti_to=noti_to, noti_type=noti_type, is_mine=is_mine)
    elif noti_type == 3 or noti_type == 4: #피드신고(1~9) or 피드숨김(10이상)
        feed = Feed.objects.get(id=fid)
        noti_from = Profile.objects.get(user_id=uid)
        noti_to = Profile.objects.get(user = feed.creator)
        Notification.objects.create(feed=feed, noti_from=noti_from, noti_to=noti_to, noti_type=noti_type)
    elif noti_type == 5: #댓글좋아요
        feedcomment = FeedComment.objects.get(id=fid)
        feed = feedcomment.feed
        noti_from = Profile.objects.get(user_id=uid)
        noti_to = Profile.objects.get(user = feedcomment.reactor)
        if noti_from != noti_to:
            is_mine = False
        else:
            is_mine = True
        Notification.objects.create(feed=feed, noti_from=noti_from, noti_to=noti_to, noti_type=noti_type, is_mine=is_mine)
    elif noti_type == 6: #구독
        noti_from = Profile.objects.get(user_id=uid)
        noti_to = Profile.objects.get(user_id=fid)
        follow = Follow.objects.get(follow_from=noti_from, follow_to=noti_to)
        Notification.objects.create(follow=follow, noti_from=noti_from, noti_to=noti_to, noti_type=noti_type)
    elif noti_type == 7: #구독새글 (서비스 커지면 이부분이 가장 부하를 줄 수 있겠음)
        feed = Feed.objects.get(id=fid)
        creator_pf = Profile.objects.get(user_id=uid)
        my_fan_subs = Follow.objects.filter(follow_to=creator_pf)
        for my_fan_sub in my_fan_subs:
            my_fan_pf = my_fan_sub.follow_from
            Notification.objects.create(feed=feed, noti_from=creator_pf, noti_to=my_fan_pf, noti_type=noti_type)
    return
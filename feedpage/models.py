from django.db import models
from faker import Faker
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from django.core.validators import MaxValueValidator, MinValueValidator
import random
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFill
import uuid

class HashTag(models.Model):
    tag = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return str(self.tag)

class Feed(models.Model):
    # null, blank 나중에 한번 정리하기
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    creator = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content_a = models.CharField(max_length=21)
    content_b = models.CharField(max_length=21)
    upvote_users = models.ManyToManyField(User, blank=True, related_name='upvote_feeds', through='Upvote')
    matched_tags = models.ManyToManyField(HashTag, blank=True, related_name='tagged_feeds', through='TagRelation')
    img_a = ProcessedImageField(
		upload_to = 'feed_img',
		processors = [ResizeToFill(730, 730)],
		format = 'JPEG',
		options = {'quality': 50},
        null = True
        )
    img_b = ProcessedImageField(
		upload_to = 'feed_img',
		processors = [ResizeToFill(730, 730)],
		format = 'JPEG',
		options = {'quality': 50},
        null = True
        )
    feed_type = models.IntegerField(default=1) # 0: 튜토리얼, 1:일반, 2:공지, 3:광고
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def check_visible(self):
        if self.report_set.count() > 9:
            visible = False
        else:
            visible = True
        return visible

    def update_date(self): 
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def seed(feed_amount, user_amount): 
        myfake = Faker('ko_KR')
        for i in range(feed_amount):
            uid = random.randrange(1,user_amount)
            Feed.objects.create(
                title = myfake.bs(),
                creator = User.objects.get(id=uid),
                content_a = myfake.catch_phrase(),
                content_b = myfake.catch_phrase(),
                img_a = '/static/feedpage/facebook_icon.png',
                img_b = '/static/feedpage/kakao_icon.png',
            )

        #되는지 다음번 db초기화때 확인필요
        for j in range(user_amount):
            for i in range(feed_amount):
                Upvote.objects.create(
                    user = User.objects.get(id=j),
                    feed = Feed.objects.get(id=i),
                    about_a = myfake.boolean(chance_of_getting_true=40),
                )

class FeedComment(models.Model):
    reactor = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content = models.CharField(max_length=70)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    upvote_side = models.IntegerField(default=0)
    upvote_users = models.ManyToManyField(User, blank=True, related_name='upvote_feedcomments', through='CommentUpvote')
    total_upvote = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.content)

class TagRelation(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    hash_tag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.hash_tag)

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    about_a = models.BooleanField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.about_a)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.feed)

class CommentUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedcomment = models.ForeignKey(FeedComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.feedcomment)

class Notification(models.Model):
    from accounts.models import Profile, Follow

    noti_from = models.ForeignKey(Profile, related_name = 'noti_from', blank=True, on_delete= models.CASCADE)
    noti_to = models.ForeignKey(Profile, related_name = 'noti_to', blank=True, on_delete= models.CASCADE)
    noti_type = models.IntegerField(default=0)
    feed = models.ForeignKey(Feed, null=True, on_delete=models.CASCADE)
    follow = models.ForeignKey(Follow, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_checked = models.BooleanField(default=False)
    is_mine = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at)
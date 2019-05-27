from django.db import models
from faker import Faker
from django.contrib.auth.models import User 
from accounts.models import Profile, Follow
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from django.core.validators import MaxValueValidator, MinValueValidator
import random

class HashTag(models.Model):
    tag = models.TextField(null=True)

    def __str__(self):
        return str(self.tag)

class Feed(models.Model):
    # null, blank 나중에 한번 정리하기
    title = models.CharField(max_length=30)
    creator = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content_a = models.CharField(max_length=30)
    content_b = models.CharField(max_length=30)
    upvote_users = models.ManyToManyField(User, blank=True, related_name='upvote_feeds', through='Upvote')
    matched_tags = models.ManyToManyField(HashTag, blank=True, related_name='tagged_feeds', through='TagRelation')
    img_a = models.ImageField(blank=True, null=True, upload_to='feed_img')
    img_b = models.ImageField(blank=True, null=True, upload_to='feed_img') #have to fix
# 수정가능여부
# 익명여부
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

    # def seed(count): 
    #     myfake = Faker('ko_KR')
    #     for i in range(count):
    #         Feed.objects.create(
    #             title = myfake.bs(),
    #             editnow = False,
    #             content_a = myfake.catch_phrase(),
    #             content_b = myfake.catch_phrase(),
    #         )

class FeedComment(models.Model):
    reactor = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content = models.TextField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    upvote_side = models.IntegerField(default=0)
    upvote_users = models.ManyToManyField(User, blank=True, related_name='upvote_feedcomments', through='CommentUpvote')
    total_upvote = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

class TagRelation(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    hash_tag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.hash_tag)

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    about_a = models.BooleanField(null=True)
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
    noti_from = models.ForeignKey(Profile, related_name = 'noti_from', null=True, on_delete= models.CASCADE)
    noti_to = models.ForeignKey(Profile, related_name = 'noti_to', null=True, on_delete= models.CASCADE)
    noti_type = models.IntegerField(default=0)
    feed = models.ForeignKey(Feed, null=True, on_delete=models.CASCADE)
    follow = models.ForeignKey(Follow, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_checked = models.BooleanField(default=False)
    is_mine = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at)
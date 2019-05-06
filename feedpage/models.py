from django.db import models
from faker import Faker
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from django.core.validators import MaxValueValidator, MinValueValidator
import random

class HashTag(models.Model):
    tag = models.TextField(null=True)
    # feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tag)

class Feed(models.Model):
    # null, blank 나중에 한번 정리하기
    title = models.CharField(max_length=256)
    creator = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content_a = models.TextField(blank=False, null=False)
    content_b = models.TextField(blank=False, null=False)
    upvote_users = models.ManyToManyField(User, blank=True, related_name='upvote_feeds', through='Upvote')
    matched_tags = models.ManyToManyField(HashTag, blank=True, related_name='tagged_feeds', through='TagRelation')
    img_a = models.ImageField(blank=True, null=True) #have to fix
    img_b = models.ImageField(blank=True, null=True) #have to fix
    upvote_a = models.IntegerField(default=0)
    upvote_b = models.IntegerField(default=0)
    report_count = models.IntegerField(default=0)
    editnow = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    def check_visible(self):
        if self.report_set.count() > 9:
            visible = False
        else:
            visible = True
        print(self.report_set.count())
        print(visible)
        return visible

    def update_date(self): 
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def seed(count): 
        myfake = Faker('ko_KR')
        for i in range(count):
            Feed.objects.create(
                title = myfake.bs(),
                editnow = False,
                content_a = myfake.catch_phrase(),
                content_b = myfake.catch_phrase(),
                upvote_a = random.randrange(0,100),
                upvote_b = random.randrange(0,100),
                report_count = random.randrange(0,4),
                # img_a = ,
                # img_b = ,
                # hash_tag = [],
            )

class FeedComment(models.Model):
    reactor = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content = models.TextField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    upvote_users = models.ManyToManyField(User, blank=True, related_name='upvote_feed_comments', through='CommentUpvote')
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
    feed_comment = models.ForeignKey(FeedComment, on_delete=models.CASCADE)
    total_upvote = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.feed_comment)
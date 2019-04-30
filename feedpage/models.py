from django.db import models
from faker import Faker
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from django.core.validators import MaxValueValidator, MinValueValidator
import random

# Create your models here.
class Feed(models.Model):
    title = models.CharField(max_length=256)
    creator = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    upvote_users = models.ManyToManyField(User, blank=True, related_name='feeds_upvote', through='Upvote')
    content_a = models.TextField(blank=False, null=False)
    content_b = models.TextField(blank=False, null=False)
    img_a = models.ImageField(blank=True, null=True) #have to fix
    img_b = models.ImageField(blank=True, null=True) #have to fix
    upvote_a = models.IntegerField(default=0)
    upvote_b = models.IntegerField(default=0)
    report = models.IntegerField(default=0)
    #hash_tag도 추가 필요
    editnow = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    def check_invisible(self):
        if self.report > 9:
            invisible = True
        else:
            invisible = False
        return invisible

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
                # upvote_a = random.randrange(0,100),
                # upvote_b = random.randrange(0,100),
                # report = random.randrange(0,4),
                # img_a = ,
                # img_b = ,
                # hash_tag = [],
            )

class FeedComment(models.Model):
    reactor = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content = models.TextField()
    # feed id를 가져야 하는, Feed:FeedComment = 1:N 관계니까
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    about_a = models.BooleanField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

class HashTag(models.Model):
    tag = models.TextField(null=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tag)

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    about_a = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
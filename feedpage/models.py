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

    def update_date(self): 
        self.updated_at = timezone.now()
        self.save()

    # def get_percentage(self):
    #     upvote_total = self.upvote_a + self.upvote_b
    #     if upvote_total > 0:
    #         perc_a = "{:.1%}".format(self.upvote_a / upvote_total)
    #         perc_b = "{:.1%}".format(self.upvote_b / upvote_total)
    #     else:
    #         perc_a = ""
    #         perc_b = ""
    #     return perc_a, perc_b

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
                report = random.randrange(0,4),
                # img_a = ,
                # img_b = ,
                # hash_tag = [],
            )
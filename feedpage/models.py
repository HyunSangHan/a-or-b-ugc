from django.db import models
from faker import Faker
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Feed(models.Model):
    # id는 자동 추가
    title = models.CharField(max_length=256)
    content = models.TextField()
    editnow = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    def update_date(self): # 나중에 수정할 때 씀
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def seed(count): # 추가
            myfake = Faker('ko_KR')
            for i in range(count):
                Feed.objects.create(
                    title=myfake.bs(),
                    editnow = False,
                    content=myfake.text()
                )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=20, blank=True)
    major = models.CharField(max_length=20, blank=True)

    def __str__(self):   # 추가
        return 'id=%d, user id=%d, college=%s, major=%s' % (self.id, self.user.id, self.college, self.major)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()
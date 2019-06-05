from django.db import models
from django.utils import timezone
from faker import Faker
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.hashers import make_password, is_password_usable
from django.dispatch import receiver 
from django.core.validators import MaxValueValidator, MinValueValidator
import random
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', through = 'Follow', blank=True, symmetrical=False)
    birthday = models.DateField(blank=True, null=True)
    is_male = models.BooleanField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile_img')
    created_at = models.DateTimeField(default=timezone.now)
    notichecked_at = models.DateTimeField(default=timezone.now)
    left_level = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    major = models.CharField(default="기타", max_length=3)
    region = models.IntegerField(
        default=8,
        validators=[MaxValueValidator(8), MinValueValidator(1)]
    )
#1 서울/경기
#2 강원
#3 충청
#4 호남
#5 영남
#6 제주
#7 해외
#8 기타
    recent_login = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    def seed(min_count, max_count):
        myfake = Faker('ko_KR')
        for i in range(min_count, max_count):
            username = myfake.name()
            email = '{}@{}.com'.format(i, i)
            password = '1234' #수정 필요???
            gender = myfake.boolean(chance_of_getting_true=20)
            birthday = myfake.date_this_century(before_today=True, after_today=False)
            politics = random.randrange(1,6)
            region = random.randrange(1,9)

            user = User.objects.create_user(
                username = username,
                password = password,
                email = email
            )

            # user.set_password('1234')
            # user.save()

            profile = user.profile
            profile.is_male = gender
            profile.birthday = birthday
            profile.left_level = politics
            profile.region = region
            profile.major = "예체능"
            profile.recent_login = timezone.now()
            profile.save()


class Follow(models.Model): 
    follow_to = models.ForeignKey(Profile, related_name = 'follow_to', on_delete=models.CASCADE)
    follow_from = models.ForeignKey(Profile, related_name = 'follow_from', on_delete=models.CASCADE)

    def __str__(self):
        return '{} follows {}'.format(self.follow_from, self.follow_to)

# @receiver(pre_save, sender=User)
# def password_hashing(instance, **kwargs):
#     if not is_password_usable(instance.password):
#         instance.password = make_password(instance.password)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()
    # 합쳐질지 확인 필요

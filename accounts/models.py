from django.db import models
from django.utils import timezone
from faker import Faker
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFill
from allauth.account.signals import user_signed_up
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    follows = models.ManyToManyField('self', through = 'Follow', blank=True, symmetrical=False)
    birth = models.IntegerField(
        null=True,
        validators=[MaxValueValidator(2019), MinValueValidator(1920)]
    )
    is_male = models.BooleanField(null=True)
    image = ProcessedImageField(
		upload_to = 'profile_img',
		processors = [ResizeToFill(120, 120)],
		format = 'JPEG',
		# options = {'quality': 50},
        blank = True,
        null = True,
        # default='/static/feedpage/default_avatar.png'
        )
    created_at = models.DateTimeField(default=timezone.now)
    notichecked_at = models.DateTimeField(default=timezone.now)
    religion = models.IntegerField(
        null=True,
        validators=[MaxValueValidator(4), MinValueValidator(1)]
    )
    left_level = models.IntegerField(
        null=True,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    major = models.CharField(max_length=3, null=True)
    region = models.IntegerField(
        null=True,
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
    likes_iphone = models.BooleanField(null=True)
    is_premium = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=True)
    is_facebook = models.BooleanField(null=True)

    def __str__(self):
        return self.user.username

    def seed(min_count, max_count):
        myfake = Faker('ko_KR')
        for i in range(min_count, max_count):
            username = myfake.name()
            email = '{}@{}.com'.format(i, i)
            password = '1234' #수정 필요???
            gender = myfake.boolean(chance_of_getting_true=20)
            birth = random.randrange(1970,2000)
            politics = random.randrange(1,6)
            region = random.randrange(1,9)
            likes_iphone = myfake.boolean(chance_of_getting_true=50)

            user = User.objects.create_user(
                username = username,
                password = password,
                email = email
            )

            profile = user.profile
            profile.is_male = gender
            profile.birth = birth
            profile.left_level = politics
            profile.region = region
            profile.major = "예체능"
            profile.recent_login = timezone.now()
            profile.likes_iphone = likes_iphone
            profile.is_premium = True
            profile.is_first_login = True
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

@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):    
    from feedpage.models import Upvote

    profile = user.profile

    if sociallogin.account.provider == 'facebook':
        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        img_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
        profile.is_facebook = True
        Upvote.objects.create(user=user, feed_id=1, about_a=True)

    elif sociallogin.account.provider == 'kakao':
        user_data = user.socialaccount_set.filter(provider='kakao')[0].extra_data
        img_url = user.socialaccount_set.first().get_avatar_url()
        gender = user_data['kakao_account']['gender']
        if gender == 'male':
            profile.is_male = True
        elif gender == 'female':
            profile.is_male = False
        profile.is_facebook = False
        Upvote.objects.create(user=user, feed_id=1, about_a=False)

    if img_url:
        name = urlparse(img_url).path.split('/')[-1]
        response = requests.get(img_url)
        if response.status_code == 200:
            profile.image.save(name, ContentFile(response.content), save=True)
    profile.save()


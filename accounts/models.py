from django.db import models
from django.utils import timezone
from faker import Faker
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    is_male = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    left_level = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
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

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()
    # 합쳐질지 확인 필요
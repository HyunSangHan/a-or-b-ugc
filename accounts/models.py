from django.db import models
from faker import Faker
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    college = models.CharField(max_length=20, blank=True)
    major = models.CharField(max_length=20, blank=True)
    # admission_year = models.IntegerField(blank=False, null=True)
    # birthday = models.DateField(blank=False, null=True)
    # is_male = models.BooleanField(blank=False, null=True)
    is_graduated = models.BooleanField(blank=False, null=True)

    def __str__(self):   # 추가
        return 'id=%d, user id=%d, college=%s, major=%s' % (self.id, self.user.id, self.college, self.major)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()
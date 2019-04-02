from django.db import models
from faker import Faker # 추가

# Create your models here.

from django.utils import timezone

# Create your models here.
class Event(models.Model):
    # id는 자동 추가
    title = models.CharField(max_length=256)
    date = models.DateTimeField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    def update_date(self): # 나중에 수정할 때 씀
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return '%s - %s' % (self.title, self.date)

    def seed(count): # 추가
            myfake = Faker('ko_KR')
            for i in range(count):
                Event.objects.create(
                    title=myfake.bs(),
                    # date=timezone.now()
                    date=myfake.date(pattern="%Y-%m-%d", end_datetime=None)
                )
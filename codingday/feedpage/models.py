from django.db import models
from faker import Faker # 추가

# Create your models here.

from django.utils import timezone # 장고는 created_at과 updated_at을 알아서 만들어 주지 않음. id는 만들어 줌

# Create your models here.
class Feed(models.Model):
    # id는 자동 추가
    title = models.CharField(max_length=256)
    content = models.TextField()
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
                    content=myfake.text()
                )
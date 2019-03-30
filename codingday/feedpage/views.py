from django.shortcuts import render
from .models import Feed # 추가. (참고: .models == feeds.models)

def index(request): # 원래 있던 index 함수 수정.
    feeds = Feed.objects.all()
    return render(request, 'feedpage/index.html', {'feeds': feeds})
from django.shortcuts import render
from .models import Feed # 추가. (참고: .models == feeds.models)
from django.shortcuts import redirect

def index(request): # 원래 있던 index 함수 수정.
    if request.method == 'GET': # index
        feeds = Feed.objects.all()
        return render(request, 'feedpage/index.html', {'feeds': feeds})
    elif request.method == 'POST': # create
        title = request.POST['title']
        content = request.POST['content']
        Feed.objects.create(title=title, content=content)
        return redirect('/feeds')


def new(request):
    return render(request, 'feedpage/new.html')

def show(request, id):
    if request.method == 'GET': # show
        feed = Feed.objects.get(id=id)
        return render(request, 'feedpage/show.html', {'feed': feed})    

def delete(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect('/feeds')
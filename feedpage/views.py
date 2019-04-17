from django.shortcuts import render
from .models import Feed # 추가. (참고: .models == feeds.models)
from django.shortcuts import redirect
from django.core.paginator import Paginator

def index(request): 
    if request.method == 'GET': # index
        feeds_all = Feed.objects.all()
        paginator = Paginator(feeds_all, 8)
        page_num = request.GET.get('page')
        feeds = paginator.get_page(page_num)
        return render(request, 'feedpage/index.html', {'feeds': feeds})
    elif request.method == 'POST': # create
        title = request.POST['title']
        content = request.POST['content']
        Feed.objects.create(title=title, content=content)
        return redirect('/feeds')

def new(request):
    feed = Feed()
    return render(request, 'feedpage/new.html', {'feed': feed})

def show(request, id):
    feed = Feed.objects.get(id=id)
    if request.method == 'GET': # show
        return render(request, 'feedpage/show.html', {'feed': feed})    
    elif request.method == 'POST': # update
        if feed.editnow:
            feed.title = request.POST['title']
            feed.content_a = request.POST['content_a']
            feed.content_b = request.POST['content_b']
            feed.editnow = False
            feed.save()
            feedall = Feed.objects.all()
            return render(request, 'feedpage/index.html', {'feeds': feedall})                
        else:
            feed.title = request.POST['title']
            feed.content_a = request.POST['content_a']
            feed.content_b = request.POST['content_b']
            feed.editnow = False
            feed.save()
            return render(request, 'feedpage/show.html', {'feed': feed})    

def delete(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect('/feeds')

def edit(request, id):
    feed = Feed.objects.get(id=id)
    if request.method == 'GET': # show
        return render(request, 'feedpage/edit.html', {'feed': feed})    

def editon(request, id):
    feed = Feed.objects.get(id=id)
    feed.editnow = True
    feed.save()
    return redirect('/feeds')

def editoff(request, id):
    feed = Feed.objects.get(id=id)
    feed.editnow = False
    feed.save()
    return redirect('/feeds')
from django.shortcuts import render
from .models import Feed # 추가. (참고: .models == feeds.models)
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q

def index(request): 
    if request.method == 'POST': # create
        title = request.POST['title']
        content_a = request.POST['content_a']
        content_b = request.POST['content_b']
        Feed.objects.create(title=title, content_a=content_a, content_b=content_b)
        return redirect('/feeds')
    else: # index
        keyword = request.GET.get('keyword', '')
        feeds_all = Feed.objects.all().order_by('-updated_at', '-created_at')
        if keyword: 
            feeds_all = feeds_all.filter(Q(title__icontains=keyword) | Q(content_a__icontains=keyword) | Q(content_b__icontains=keyword))
        paginator = Paginator(feeds_all, 8)
        page_num = request.GET.get('page')
        feeds = paginator.get_page(page_num)
        search_result_num = len(feeds_all)
        if keyword and feeds:
            is_searched = True
        elif keyword == '':
            is_searched = False
        else:
            is_searched = True
        return render(request, 'feedpage/index.html', {'feeds': feeds, 'keyword': keyword, 'page': page_num, 'is_searched': is_searched, 'search_result_num': search_result_num})
#문제1: page1일때 next 파라미터를 못넘김
#문제2: page2부터는 next 파라미터를 잘 넘기는데도 활용되지 못하고 있음

def new(request):
    feed = Feed()
    return render(request, 'feedpage/new.html', {'feed': feed})

def show(request, id):
    feed = Feed.objects.get(id=id)
    if request.method == 'POST': # update
        feed.title = request.POST['title']
        feed.content_a = request.POST['content_a']
        feed.content_b = request.POST['content_b']
        feed.editnow = False
        feed.save()
        return redirect('/feeds')
    else: # show
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
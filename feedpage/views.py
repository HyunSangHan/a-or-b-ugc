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
    elif request.method == 'PUT': # update
        title = request.PUT['title']
        content = request.PUT['content']
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
        feed.title = request.POST['title']
        feed.content = request.POST['content']
        feed.save()
        return render(request, 'feedpage/show.html', {'feed': feed})    
################## How can I use PUT method her???

def delete(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect('/feeds')

def edit(request, id):
    feed = Feed.objects.get(id=id)
    if request.method == 'GET': # show
        return render(request, 'feedpage/edit.html', {'feed': feed})    
#     if request.method == "POST":
#         # feed = feed_tmp.save(commit=False)
#         feed.title = request.POST['title']
#         feed.content = request.POST['content']
#         feed.save()
#         return render(request, 'feedpage/edit.html', {'feed': feed})    



# def edit(request, id):
#     feed = Feed.objects.get(id=id)
#     if request.method == "POST":
#         # feed = feed_tmp.save(commit=False)
#         feed.title = request.POST['title']
#         feed.content = request.POST['content']
#         feed.save()
#         return render(request, 'feedpage/show.html', {'feed': feed})    


# def edit(request, id):
# #     if request.method == 'GET': # show editor 
#     feed = Feed.objects.get(id=id)
#     if request.method == "POST":
#         feed_tmp = Feed(instance=feed)
#         if feed_tmp.is_vaild():
#             feed = feed_tmp.save(commit=False)
#             feed.title = request.title
#             feed.content = request.content
#             feed.save()
#             return render(request, 'feedpage/new.html', {'feed': feed})    

# def edit(request, id):
#     if request.method == 'POST': # edit
#         feed = Feed.objects.get(id=id)
#         feed.title = request.POST['title']
#         feed.content = request.POST['content']
#         feed.save()
#         return redirect('/feeds')
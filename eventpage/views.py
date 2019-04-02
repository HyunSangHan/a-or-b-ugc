from django.shortcuts import render
from .models import Event 
from django.shortcuts import redirect
from django.utils import timezone

def event(request): 
    if request.method == 'GET': 
        events = Event.objects.all()
        return render(request, 'eventpage/event.html', {'events': events})
    elif request.method == 'POST':
        title = request.POST['title']
        date = timezone.now()
        Event.objects.create(title=title, date=date)
        return redirect('/events')


def new(request):
    event = Event()
    return render(request, 'eventpage/new.html', {'event': event})

def delete(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('/events')
from django.urls import path
from eventpage import views

urlpatterns = [
    path('', views.event, name='event'),
    path('new/', views.new, name='new'), 
    path('<int:id>/delete/', views.delete, name='delete'),
]
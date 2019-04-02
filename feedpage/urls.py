from django.urls import path
from feedpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'), 
    path('<int:id>/', views.show, name='show'), 
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/editon/', views.editon, name='editon'),
    path('<int:id>/editoff/', views.editoff, name='editoff'),
]
from django.urls import path
from feedpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'), # 추가
    path('<int:id>/', views.show, name='show'), # 추가
    path('<int:id>/delete', views.delete, name='delete') #추가
]
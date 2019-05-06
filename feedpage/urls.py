from django.urls import path
from feedpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'), 
    path('<int:id>/', views.show, name='show'), 
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/delete_tag/<int:tid>/', views.delete_tag, name='delete_tag'),
    path('<int:id>/editon/', views.editon, name='editon'),
    path('<int:id>/editoff/', views.editoff, name='editoff'),
    path('<int:id>/comments/', views.create_comment, name='create_comment'),
    path('<int:id>/comments/<int:cid>/', views.delete_comment, name='delete_comment'),
    path('<int:id>/comments/<int:cid>/upvote', views.upvote_comment, name='upvote_comment'),
    path('<int:pk>/upvote_a/', views.feed_upvote_a, name='upvote_a'),
    path('<int:pk>/upvote_b/', views.feed_upvote_b, name='upvote_b'),
    path('<int:pk>/report/', views.report, name='report'),
    path('<int:pk>/follow/', views.follow_manager, name='follow'),
]
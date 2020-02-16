from django.urls import path
from feedpage import views

# pk or id

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/', views.index_ajax, name='index_ajax'),
    path('new/', views.new, name='new'), 
    path('<uuid:uuid>/', views.show, name='show'), 
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<uuid:uuid>/edit/', views.edit, name='edit'),
    path('<int:id>/delete_tag/<int:trid>/', views.delete_tag, name='delete_tag'),
    path('<int:id>/comments/', views.create_comment, name='create_comment'),
    path('<int:id>/comments/<int:cid>/', views.delete_comment, name='delete_comment'),
    path('<int:id>/comments/<int:cid>/upvote', views.upvote_comment, name='upvote_comment'),
    path('<int:pk>/upvote_A/', views.feed_upvote_a, name='upvote_a'),
    path('<int:pk>/upvote_B/', views.feed_upvote_b, name='upvote_b'),
    path('<int:pk>/report/', views.report, name='report'),
    path('<int:pk>/follow/', views.follow_manager, name='follow'),
    path('<int:pk>/statistics/<stat_menu>/<stat_name>/', views.statistics, name='statistics'),
    path('creator/<creator_name>/', views.creator, name='creator'),
    path('creator/<creator_name>/ajax/', views.creator_ajax, name='creator_ajax'),
    path('mysubscribe/', views.mysubscribe, name='mysubscribe'), 
    path('myreaction/', views.myreaction, name='myreaction'), 
    path('mynotification/', views.mynotification, name='mynotification'), 
    path('new/image_search/', views.image_search, name='image_search'),
]
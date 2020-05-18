"""snulion7th URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# import feedpage.views
from django.conf.urls import include
import accounts.views
import feedpage.views
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', feedpage.views.index, name='index'),
    path('ajax/', feedpage.views.index_ajax, name='index_ajax'),
    path('new/', feedpage.views.new, name='new'), 
    path('<uuid:uuid>/', feedpage.views.show, name='show'), 
    path('<int:id>/delete/', feedpage.views.delete, name='delete'),
    path('<uuid:uuid>/edit/', feedpage.views.edit, name='edit'),
    path('<int:id>/delete_tag/<int:trid>/', feedpage.views.delete_tag, name='delete_tag'),
    path('<int:id>/comments/', feedpage.views.create_comment, name='create_comment'),
    path('<int:id>/comments/<int:cid>/', feedpage.views.delete_comment, name='delete_comment'),
    path('<int:id>/comments/<int:cid>/upvote', feedpage.views.upvote_comment, name='upvote_comment'),
    path('<int:pk>/upvote_A/', feedpage.views.feed_upvote_a, name='upvote_a'),
    path('<int:pk>/upvote_B/', feedpage.views.feed_upvote_b, name='upvote_b'),
    path('<int:pk>/report/', feedpage.views.report, name='report'),
    path('<int:pk>/follow/', feedpage.views.follow_manager, name='follow'),
    path('<int:pk>/statistics/<stat_menu>/<stat_name>/', feedpage.views.statistics, name='statistics'),
    path('creator/<creator_name>/', feedpage.views.creator, name='creator'),
    path('creator/<creator_name>/ajax/', feedpage.views.creator_ajax, name='creator_ajax'),
    path('mysubscribe/', feedpage.views.mysubscribe, name='mysubscribe'), 
    path('mysubscribe/ajax/', feedpage.views.mysubscribe_ajax, name='mysubscribe_ajax'), 
    path('myreaction/', feedpage.views.myreaction, name='myreaction'), 
    path('myreaction/ajax/', feedpage.views.myreaction_ajax, name='myreaction_ajax'), 
    path('mynotification/', feedpage.views.mynotification, name='mynotification'), 
    path('mynotification/ajax/', feedpage.views.mynotification_ajax, name='mynotification_ajax'), 
    path('new/image_search/', feedpage.views.image_search, name='image_search'),
    path('accounts/', include('accounts.urls')),
    path('social_accounts/', include('allauth.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/signup/', accounts.views.signup, name='signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
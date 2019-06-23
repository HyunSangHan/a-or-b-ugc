from django.contrib import admin
from .models import Feed, FeedComment, Report
# Register your models here.

admin.site.register(Feed)
admin.site.register(FeedComment)
admin.site.register(Report)
from django.contrib import admin
from .models import Feed, FeedComment, Report, HashTag, TagRelation
# Register your models here.

admin.site.register(Feed)
admin.site.register(FeedComment)
admin.site.register(Report)
admin.site.register(HashTag)
admin.site.register(TagRelation)
from django.contrib import admin
from .models import Feed, FeedComment, Report, HashTag, TagRelation, Upvote, CommentUpvote
# Register your models here.

admin.site.register(Feed)
admin.site.register(Upvote)
admin.site.register(FeedComment)
admin.site.register(CommentUpvote)
admin.site.register(Report)
admin.site.register(HashTag)
admin.site.register(TagRelation)
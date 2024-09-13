from django.contrib import admin
from .models import VirtualMemories, Comment, ReplyComment


class VirtualMemoriesAdmin(admin.ModelAdmin):
    list_display = ['note', 'Add_tag', 'feed_date', 'username', 'name']
    list_filter = ['feed_date', 'Add_tag']
    search_fields = ['author__app_user__username', 'author__app_user__first_name', 'author__app_user__last_name', 'id']
    list_per_page = 20

    def note(self, obj):
        if len(obj.Add_note) > 50:
            return obj.Add_note[:50] + '.....'
        return obj.Add_note[:50]

    def name(self, obj):
        return f'{obj.author.app_user.first_name} {obj.author.app_user.last_name}'

    def username(self, obj):
        return f'{obj.author.app_user}'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_person', 'comment_short', 'comment_date', 'on_feed']
    list_filter = ['comment_person', 'comment_date']
    search_fields = ['comment_person__username', 'parent_feed__Add_note', 'comment', 'id']
    list_per_page = 20

    def comment_short(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + '.....'
        return obj.comment[:50]

    def on_feed(self, obj):
        if len(obj.parent_feed.Add_note) > 50:
            return obj.parent_feed.Add_note[:50] + '..... ~' + obj.parent_feed.author.app_user.username
        return obj.parent_feed.Add_note[:50] + '~' + obj.parent_feed.author.app_user.username


class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ['comment_reply_person', 'reply_short', 'comment_reply_date', 'on_comment']
    list_filter = ['comment_reply_person', 'comment_reply_date']
    search_fields = ['comment_reply_person__username', 'parent_comment__comment', 'reply', 'id']
    list_per_page = 20

    def reply_short(self, obj):
        if len(obj.reply) > 50:
            return obj.reply[:50] + '.....'
        return obj.reply[:50]

    def on_comment(self, obj):
        if len(obj.parent_comment.comment) > 50:
            return obj.parent_comment.comment[:50] + '..... ~' + obj.parent_comment.comment_person.username
        return obj.parent_comment.comment[:50] + '~' + obj.parent_comment.comment_person.username


admin.site.register(VirtualMemories, VirtualMemoriesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommentAdmin)

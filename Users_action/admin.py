from django.contrib import admin
from .models import Profile, UserProjects, SendEmail, contactForm
from django.contrib.auth.models import Group
from django.utils.html import format_html

class contactFormAdmin(admin.ModelAdmin):
    list_display = ['sender', 'sender_email', 'content']
    list_filter = ['sender']
    search_fields = ['sender__username', 'sender_email']
    list_per_page = 30

    def content(self, obj):
        if len(obj.content)>50:
            return format_html(f'{obj.content[:120]}....')
        else:
            return format_html(f'{obj.content}')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['app_user', 'current_status', 'name']
    list_filter = ['current_status', 'date_join']
    search_fields = ['app_user__username', 'app_user__first_name', 'app_user__last_name', 'id']
    list_per_page = 20

    def name(self, obj):
        return f'{obj.app_user.first_name} {obj.app_user.last_name}'


class UserProjectsAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'projects_author', 'name']
    list_filter = ['projects_author']
    search_fields = ['projects_author__username', 'projects_author__first_name', 'projects_author__last_name', 'id']
    list_per_page = 20

    def name(self, obj):
        return f'{obj.projects_author.first_name} {obj.projects_author.last_name}'


class sendEmailAdmin(admin.ModelAdmin):
    list_display = ['email_subject', 'body1', 'sender']

    def body1(self, obj):
        if len(obj.body)>50:
            return format_html(f'{obj.body[:120]}....')
        else:
            return format_html(f'{obj.body}')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserProjects, UserProjectsAdmin)
admin.site.unregister(Group)
admin.site.register(SendEmail, sendEmailAdmin)
admin.site.register(contactForm, contactFormAdmin)
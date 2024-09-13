from django.contrib import admin
from .models import Posts, Posts_Category


class PostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'Category', 'date_posted']
    list_filter = ['date_posted', 'Category']
    search_fields = ['Title', 'author__username', 'Category__Category_name', 'date_posted']
    list_per_page = 20

    def title(self, obj):
        if len(obj.Title) > 50:
            return obj.Title[:50] + '.....'
        return obj.Title[:50]


admin.site.register(Posts, PostsAdmin)
admin.site.register(Posts_Category)
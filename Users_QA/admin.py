from django.contrib import admin
from .models import FieldCategory, Field_Q, Field_Q_A
from django.utils.html import format_html


class FieldCategoryAdmin(admin.ModelAdmin):
    list_display = ['field_name', 'about_field', 'filed_interst']

    def name(self, obj):
        return f'{obj.app_user.first_name} {obj.app_user.last_name}'

    def filed_interst(self, obj):
        return f'{obj.field_likes.count()}'


class Field_QAdmin(admin.ModelAdmin):
    list_display = ['question_s', 'parent_field', 'q_person', 'q_date']
    search_fields = ['question', 'parent_field__field_name', 'q_person__username', 'id']
    list_filter = ['parent_field', 'q_date']
    list_per_page = 20

    def question_s(self, obj):
        if len(obj.question)>50:
            return format_html(f'{obj.question[:50]}....')
        else:
            return format_html(f'{obj.question}')


class Field_Q_A_Admin(admin.ModelAdmin):
    list_display = ['ans_s', 'a_person', 'a_date', 'question']
    search_fields = ['parent_q__question', 'answer', 'a_person__username', 'id']
    list_filter = ['a_person', 'a_date']
    list_per_page = 20

    def ans_s(self, obj):
        if len(obj.answer)>50:
            return format_html(f'{obj.answer[:50]}....')
        else:
            return format_html(f'{obj.answer}')

    def question(self, obj):
        if len(obj.parent_q.question)>50:
            return format_html(f'{obj.parent_q.question[:50]}....~{obj.parent_q.q_person.username}')
        else:
            return format_html(f'{obj.parent_q.question} ~<b style="margin:0px;">{obj.parent_q.q_person.username}</b>')



admin.site.register(FieldCategory, FieldCategoryAdmin)
admin.site.register(Field_Q, Field_QAdmin)
admin.site.register(Field_Q_A, Field_Q_A_Admin)
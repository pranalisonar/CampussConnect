from django.contrib import admin
from .models import QuestionPapers


class QuestionPapersAdmin(admin.ModelAdmin):
    list_display = ['Subject_name', 'Class_year', 'Exam_pattern', 'exam_date', 'Upload_date', 'Uploader']
    list_filter = ['Class_year', 'Subject_name', 'Exam_pattern', 'Upload_date']
    search_fields = ['Subject_name', 'Exam_pattern', 'Uploader__username', 'Class_year', 'id']
    list_per_page = 20

    def exam_date(self, obj):
        return f'{obj.Exam_Month} {obj.Exam_Year}'

admin.site.register(QuestionPapers, QuestionPapersAdmin)
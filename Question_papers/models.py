from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


class QuestionPapers(models.Model):
    Uploader = models.ForeignKey(User, related_name='AllQuestionPaper', on_delete=models.SET_DEFAULT, default=1)
    Subject_name = models.CharField(max_length=60)
    Class_year = models.CharField(max_length=20, default='Unknown')
    Exam_pattern = models.CharField(max_length=15, default='Unknown')
    Question_paper = models.FileField(upload_to='Question_Paper',
                                      validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    Exam_Month = models.CharField(max_length=10, default='Unknown')
    Exam_Year = models.CharField(max_length=4, default='2000')
    Upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.Subject_name}_{self.Exam_Month} {self.Exam_Year} by - {self.Uploader}"
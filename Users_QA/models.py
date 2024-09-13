from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import reverse
from django.utils.html import format_html

class FieldCategory(models.Model):
    field_name = models.CharField(max_length=30, default='global')
    logo_filed = models.ImageField(upload_to='Category_logo', default='category_default.png')
    about_field = models.CharField(max_length=230, default='tap the button to see question(s).')
    field_likes = models.ManyToManyField(User, related_name='field_like', blank=True)

    def __str__(self):
        return f"{self.field_name}"



class Field_Q(models.Model):
    parent_field = models.ForeignKey(FieldCategory, default=1, on_delete=models.SET_DEFAULT, related_name='questions')
    q_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_questions')

    q_date = models.DateField(default=timezone.now)
    q_likes = models.ManyToManyField(User, blank=True, related_name='self_q_likes')
    question = RichTextField(max_length=6000)

    def get_absolute_url(self):
        return reverse('field-questions', kwargs={'pk': self.parent_field.id})

    def __str__(self):
        return format_html(f"Category: {self.parent_field}  questoin: {self.question}")



class Field_Q_A(models.Model):
    parent_q = models.ForeignKey(Field_Q, on_delete=models.CASCADE, related_name='answer')
    a_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_answer')

    a_date = models.DateField(default=timezone.now)
    a_likes = models.ManyToManyField(User, blank=True, related_name='self_a_likes')
    answer = RichTextField()


    def get_absolute_url(self):
        return reverse('questions-ans', kwargs={'pk': self.parent_q.id})

    def __str__(self):
        return f"{self.parent_q}  answering person :-{self.a_person}"
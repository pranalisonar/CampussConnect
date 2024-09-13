from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Posts_Category(models.Model):
    Category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Category_name


class Posts(models.Model):
    Title = models.CharField(max_length=120, null=False, blank=False)
    Describe_content = models.CharField(max_length=220, null=True, blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    Content = RichTextField()

    Category = models.ForeignKey(Posts_Category, default=1, on_delete=models.SET_DEFAULT, blank=False)
    likes = models.ManyToManyField(User, related_name='blog_post', blank=True)

    author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)

    def get_absolute_url(self):
        return reverse('post_detail',  kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.Title
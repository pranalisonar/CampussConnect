from PIL import Image
from django.db import models
from django.utils import timezone
from Users_action.models import Profile
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.urls import reverse


class VirtualMemories(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Add_tag = models.CharField(max_length=40)
    Add_note = models.TextField(1500)
    Add_file = models.FileField(upload_to='VirtualMemory', validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])])
    feed_date = models.DateTimeField(default=timezone.now)
    feed_likes = models.ManyToManyField(User, related_name='feed_post_like', blank=True)

    def get_absolute_url(self):
        return reverse('feed_comments',  kwargs={'pk': self.id})

    def __str__(self):
        return f'{self.Add_tag} - {self.author.app_user.username}'

    def save(self, *args, **kwargs):
        super(VirtualMemories, self).save(*args, **kwargs)

        img1 = Image.open(self.Add_file.path)
        if img1.height > 1000 or img1.width > 1000:
            output_size = (1000, 1000)
            img1.thumbnail(output_size)
            img1.save(self.Add_file.path)


class Comment(models.Model):
    parent_feed = models.ForeignKey(VirtualMemories, on_delete=models.CASCADE, related_name='comment_model')
    comment_person = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(1000)

    def get_absolute_url(self):
        return reverse('feed_comments',  kwargs={'pk': self.parent_feed.id})

    def __str__(self):
        return f"{self.comment_person} ON -- {self.parent_feed.id} - {self.comment[:70]}.... "


class ReplyComment(models.Model):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='reply_model')
    comment_reply_person = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_reply_date = models.DateTimeField(default=timezone.now)
    reply = models.TextField(1000)

    def get_absolute_url(self):
        return reverse('reply_comment', kwargs={'pk': self.parent_comment.id})

    def __str__(self):
        return f"{self.comment_reply_person} --- [{self.reply}] "
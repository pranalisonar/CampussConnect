from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.core.validators import FileExtensionValidator

class contactForm(models.Model):
    content = models.TextField(max_length=2000, null=False)
    sender = models.ForeignKey(User, related_name='contactPerson', on_delete=models.SET_NULL, null=True)
    sender_email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return f"{self.sender} {self.sender_email}"


class SendEmail(models.Model):
    email_subject = models.CharField(max_length=120, null=True)
    body = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.email_subject}"


class UserProjects(models.Model):
    projects_author = models.ForeignKey(User, default=1, on_delete=models.CASCADE, blank=True)
    project_title = models.CharField(max_length=250, null=True, blank=False)
    project_journey = RichTextField()

    def __str__(self):
        return f"{self.project_title}"

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})


class Profile(models.Model):
    app_user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_status = models.CharField(max_length=50, default='Student')
    user_image = models.ImageField(default='d304cd17231971fad58cab69d27a7e4eace197d7My_profile.jpg',
                                   upload_to='profile_pics', help_text='500x500 is best.')
    user_resume = models.FileField(upload_to='resumes',
                                   validators=[FileExtensionValidator(allowed_extensions=['docx', 'doc'])],
                                   help_text='only docx and doc files allowed.',
                                   null=True, blank=True)
    follow = models.ManyToManyField(User, related_name="follwers", blank=True)

    date_join = models.DateField(default=timezone.now)

    Web_url = models.CharField(max_length=120, default="#", blank=True)
    Github_url = models.CharField(max_length=120, default="#", blank=True)
    Linkedin_url = models.CharField(max_length=120, default="#", blank=True)
    Insta_url = models.CharField(max_length=120, default="#", blank=True)
    Fb_url = models.CharField(max_length=120, default="#", blank=True)

    def __str__(self):
        return f'{self.app_user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img1 = Image.open(self.user_image.path)
        if img1.height > 400 or img1.width > 400:
            output_size = (400, 400)

            img1.thumbnail(output_size)
            img1.save(self.user_image.path)
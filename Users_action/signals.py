from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from Users_feeds.models import VirtualMemories
from Question_papers.models import QuestionPapers
from Users_QA.models import FieldCategory
from main.models import Posts
from django.shortcuts import get_object_or_404
from CampusConnect.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import os


# -------/-/-/-/-/-/-/-/-/-/- For new blog -/-/-/-/-/-/-/-/-/-/-/-/----------- #
# when User create new blog send email to their followers.
@receiver(signal=post_save, sender=Posts)
def sendEmailToFollowers(sender, instance, created, **kwargs):
    author = instance.__class__.objects.get(id=instance.id)
    profile = get_object_or_404(Profile, app_user=author.author)
    receiver_user = []

    for user in profile.follow.all():
        receiver_user.append(user.email)
    if len(receiver_user) > 0:
        try:
            send_mail(
                f'New blog by {instance.author}',
                f"Hi {instance.author} sheared new blog of title \n\n'{instance.Title}.'\n\nCheck out what they sheared with you all.\n\n\n You get this email because you followed {instance.author}\n thank you.",
                EMAIL_HOST_USER,
                receiver_user,
                fail_silently=False,
            )
        except:
            pass
    del receiver_user


# -------/-/-/-/-/-/-/-/-/-/- For User Profile section -/-/-/-/-/-/-/-/-/-/-/-/----------- #
# when User get created then create its profile
@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(app_user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



# -------/-/-/-/-/-/-/-/-/-/- For Profile Pic section -/-/-/-/-/-/-/-/-/-/-/-/----------- #
# When we update image then delete old image
@receiver(pre_save, sender=Profile)
def pre_save_image(sender, instance, *args, **kwargs):
    try:
        old_img_name = instance.__class__.objects.get(id=instance.id).user_image.name

        old_img = instance.__class__.objects.get(id=instance.id).user_image.path

        try:
            new_img = instance.user_image.path
        except:
            new_img = None

        if new_img != old_img:
            if os.path.exists(old_img):
                if old_img_name == 'd304cd17231971fad58cab69d27a7e4eace197d7My_profile.jpg':
                    pass
                else:
                    os.remove(old_img)
    except:
        pass

# when user delete its profile pic also delete it form the media folder.
@receiver(post_delete, sender=Profile)
def Post_delete_image(sender, instance, *args, **kwargs):
    try:
        old_img_name = instance.__class__.objects.get(id=instance.id).user_image.name
        if old_img_name == 'd304cd17231971fad58cab69d27a7e4eace197d7My_profile.jpg':
            pass
        else:
            instance.user_image.delete(save=False)
    except:
        pass



# -------/-/-/-/-/-/-/-/-/-/- for resume section -/-/-/-/-/-/-/-/-/-/-/-/----------- #
# When we update resume then delete old resume
@receiver(pre_save, sender=Profile)
def pre_save_resume(sender, instance, *args, **kwargs):
    try:
        old_resume = instance.__class__.objects.get(id=instance.id).user_resume.path
        try:
            new_resume = instance.user_resume.path
        except:
            new_resume = None

        if new_resume != old_resume:
            if os.path.exists(old_resume):
                os.remove(old_resume)
    except:
        pass

# when user deleted also delete it's resume.
@receiver(post_delete, sender=Profile)
def Post_delete_resume(sender, instance, *args, **kwargs):
    try:
        instance.user_resume.delete(save=False)
    except:
        pass


# -------/-/-/-/-/-/-/-/-/-/- For Virtual memory section -/-/-/-/-/-/-/-/-/-/-/-/----------- #
# When we update file then delete old file
@receiver(pre_save, sender=VirtualMemories)
def pre_save_file(sender, instance, *args, **kwargs):
    try:
        old_file = instance.__class__.objects.get(id=instance.id).Add_file.path
        try:
            new_file = instance.Add_file.path
        except:
            new_file = None

        if new_file != old_file:
            if os.path.exists(old_file):
                os.remove(old_file)
    except:
        pass

# when user delete its memories also delete it form the media folder.
@receiver(post_delete, sender=VirtualMemories)
def Post_delete_file(sender, instance, *args, **kwargs):
    try:
        instance.Add_file.delete(save=False)
    except:
        pass



# -------/-/-/-/-/-/-/-/-/-/- For Question paper section -/-/-/-/-/-/-/-/-/-/-/-/----------- #
# When we update Question paper then delete old Question paper
@receiver(pre_save, sender=QuestionPapers)
def pre_save_qp(sender, instance, *args, **kwargs):
    try:
        old_qp = instance.__class__.objects.get(id=instance.id).Question_paper.path
        try:
            new_qp = instance.Question_paper.path
        except:
            new_qp = None

        if new_qp != old_qp:
            if os.path.exists(old_qp):
                os.remove(old_qp)
    except:
        pass

# when user delete its Question paper also delete it form the media folder.
@receiver(post_delete, sender=QuestionPapers)
def Post_delete_qp(sender, instance, *args, **kwargs):
    try:
        instance.Question_paper.delete(save=False)
    except:
        pass


# -------/-/-/-/-/-/-/-/-/-/- For Question field category logo section -/-/-/-/-/-/-/-/-/-/-/-/----------- #
# When we update Question field category logo then delete old Question paper
@receiver(pre_save, sender=FieldCategory)
def pre_save_qp(sender, instance, *args, **kwargs):
    try:
        old_img_name = instance.__class__.objects.get(id=instance.id).logo_filed.name
        old_qplogo = instance.__class__.objects.get(id=instance.id).logo_filed.path
        try:
            new_qplogo = instance.logo_filed.path
        except:
            new_qplogo = None

        if new_qplogo != old_qplogo:
            if os.path.exists(old_qplogo):
                if old_img_name == 'category_default.png':
                    pass
                else:
                    os.remove(old_qplogo)
    except:
        pass

# when user delete its Question paper also delete it form the media folder.
@receiver(post_delete, sender=FieldCategory)
def Post_delete_qp(sender, instance, *args, **kwargs):
    try:
        old_img_name = instance.__class__.objects.get(id=instance.id).logo_filed.name
        if old_img_name == 'category_default.png':
            pass
        else:
            instance.logo_filed.delete(save=False)
    except:
        pass

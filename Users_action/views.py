import os
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views import View
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import logout
from main.models import Posts
from .forms import UserRegisterForm, UserUpdateForm, UserProfileUpdateForm, SendEmailForm, contact_form
from .utils import token_generator
from .models import UserProjects
from .models import Profile as M_Profile
from CampusConnect.settings import EMAIL_HOST_USER


@login_required
def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('Home')  # Replace 'login' with your desired redirect page name

# send email to all
@login_required
def SendEmailToAll(request):
    staffs = User.objects.filter(is_staff=True)

    if request.user in staffs:
        receiver_user = []
        allUser = get_user_model().objects.all()
        for user in allUser:
            if user.is_active:
                receiver_user.append(user.email)
        print(receiver_user)

        if request.method == "POST":
            form = SendEmailForm(request.POST)
            if form.is_valid():
                Fsave = form.save()
                Fsave.sender = request.user
                Fsave.save()
                
                email_subject = form.cleaned_data.get('email_subject')
                email_body = form.cleaned_data.get('body')
                try:
                    def sendPromotionalEmail(email_sub, body):
                        send_mail(
                            email_sub,
                            body,
                            EMAIL_HOST_USER,
                            receiver_user,
                            fail_silently=False,
                        )

                    sendPromotionalEmail(email_subject, email_body)
                    messages.success(request, 'Mail sent.')
                except:
                    messages.success(request, "can't send email.")
        else:
            form = SendEmailForm()
        return render(request, 'Users_action/send_email.html', {'form': form, 'T_title': 'send-email'})
    else:
        return HttpResponse("<h1>You don't have access to this page</h1>")


def contact(request):
    if request.method == "POST":
        form = contact_form(request.POST)

        if form.is_valid():
            temp = form.save()
            temp.sender = request.user
            temp.sender_email = request.user.email
            temp.save()

            email_body = form.cleaned_data.get('content')
            try:
                def sendPromotionalEmail(body):
                    send_mail(
                        'Contact Request CampusConnect',
                        body,
                        EMAIL_HOST_USER,
                        ['swapnilbhavsar2001@gmail.com'],
                        fail_silently=False,
                    )

                sendPromotionalEmail(email_body)
                return HttpResponse("<h1>your request has been sent, we will contact you in 2, 3 days</h1>")
            except:
                return HttpResponse("<h1>we will contact you in 2, 3 days.</h1>")
    else:
        form = contact_form()
    return render(request, 'Users_action/contact.html', {'form': form, 'T_title': 'contact-page'})


# register new user.
def Register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()  # default to non-active
            user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Sending email to newly register user.
            # path to view
            domain = get_current_site(request).domain  # get domain we are on
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = 'http://' + domain + link
            email_body = f"Hi {username},\n\nYour registration to MyCollegeApplication was successful. \n\nPlease click on the bellow link to activate your account!\n {activate_url} \n\n\n\nThank You."
            try:
                send_mail(
                    'Account activation',
                    email_body,
                    EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f'Account created for {username}')
                messages.success(request, f'Please check your email for next step.')
            except:
                messages.success(request, f"can't send link.")
                messages.success(request, f"contact to admin.")
    else:
        form = UserRegisterForm()
    return render(request, 'Users_action/register.html', {'form': form, 'T_title': 'register'})


# activating user.
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            ids = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=ids)

            if not token_generator.check_token(user, token):
                messages.success(request, 'account activated already')
                return redirect('login')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'account activated')
            return redirect('login')

        except Exception as e:
            pass
        return redirect('login')


# for author's profile
@login_required
def Profile(request):
    context = UserProjects.objects.filter(projects_author=request.user.id)
    blog_count = len(Posts.objects.filter(author=request.user.id))
    return render(request, 'Users_action/profile.html', {'projects': context, 'blog_count': blog_count})


# profile update.
@login_required
def Profile_update(request, pk, name):
    try:
        if request.user.id == pk:
            if request.method == "POST":
                UserUpdate = UserUpdateForm(request.POST, instance=request.user)
                UserProfileUpdate = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

                if UserUpdate.is_valid() and UserProfileUpdate.is_valid():
                    UserUpdate.save()
                    UserProfileUpdate.save()
                    messages.success(request, f'Account has updated...')
                    return redirect('profile')
            else:
                UserUpdate = UserUpdateForm(instance=request.user)
                UserProfileUpdate = UserProfileUpdateForm(instance=request.user.profile)

            context = {
                'U_form': UserUpdate,
                'P_form': UserProfileUpdate
            }
            return render(request, 'Users_action/updateprofile.html', context)
    except:
        return HttpResponse("<h1>request forbidden</h1>")
    return HttpResponse("<h1>request forbidden</h1>")


# for random person
@login_required
def profile_info(request, pk):
    profile = M_Profile.objects.get(id=pk)
    projects = UserProjects.objects.filter(projects_author=profile.app_user.id)

    follow = False
    if profile.follow.filter(id=request.user.id).exists():
        follow = True
    blog_count = len(Posts.objects.filter(author=profile.app_user.id))
    return render(request, 'Users_action/profile_info.html',
                  {'profile': profile, 'projects': projects, 'follow': follow, 'blog_count': blog_count})


# search profile
@login_required
def searchProfiles(request):
    if request.method == 'POST':
        searched = request.POST['searchProfile']
        allProfile = M_Profile.objects.filter(
            Q(app_user__username__icontains=searched) | Q(current_status__icontains=searched)
            | Q(app_user__first_name__icontains=searched) | Q(app_user__last_name__icontains=searched))
        return render(request, 'Users_action/profileResults.html',
                      {'searched': searched, 'allProfile': allProfile, 'T_title': 'Search profile'})
    else:
        return render(request, 'Users_action/profileResults.html')

# wrapper fun for search profile.
@login_required
def wrapper(request):
    randomProfile = M_Profile.objects.all()
    return render(request, 'Users_action/wrapperSearch.html', {'randomProfiles': randomProfile, 'total': len(randomProfile)})


# Follow User Function.
@login_required
def followUser(request, pk):
    _profile = get_object_or_404(M_Profile, id=request.POST.get('profile_id'))

    if _profile.follow.filter(id=request.user.id).exists():
        _profile.follow.remove(request.user)
        messages.success(request, f'Unfollowed')
    else:
        _profile.follow.add(request.user)
        messages.success(request, f'following')

    return HttpResponseRedirect(reverse('profile_info', kwargs={'pk': pk}))

@login_required
def displayFollowers(request, pk):
    profile = get_object_or_404(M_Profile, id=pk)
    users = profile.follow.all()
    return render(request, 'Users_action/followers.html', {'followers': users})


@login_required
def download_resume(request, pk):
    ResumeProfile = get_object_or_404(M_Profile, app_user=pk)
    path = ResumeProfile.user_resume.path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


@login_required
def Project_detail_view(request, pk):
    context = UserProjects.objects.get(id=pk)
    return render(request, 'Users_action/project_detail.html', {'project': context, 'T_title': 'ProjectDetail'})


class AddProjectView(LoginRequiredMixin, CreateView):
    model = UserProjects
    fields = ['project_title', 'project_journey']

    def form_valid(self, form):
        form.instance.projects_author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddProjectView, self).get_context_data(**kwargs)
        context['T_title'] = 'AddProject'
        return context


class DeleteProjectView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserProjects
    context_object_name = 'project'
    template_name = 'main/posts_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.projects_author:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(DeleteProjectView, self).get_context_data(**kwargs)
        context['T_title'] = 'DeleteProject'
        return context


class UpdateProjectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProjects
    fields = ['project_title', 'project_journey']

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.projects_author:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.projects_author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateProjectView, self).get_context_data(**kwargs)
        context['T_title'] = 'UpdateProject'
        return context

from django.db.models import Count
from django.shortcuts import get_object_or_404, HttpResponseRedirect, reverse
from .models import VirtualMemories, Comment, ReplyComment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# all memories.
class FeedsListView(ListView):
    model = VirtualMemories
    context_object_name = 'feeds'
    template_name = 'Users_feeds/feed.html'
    ordering = ['-feed_date']

    def get_context_data(self, **kwargs):
        context = super(FeedsListView, self).get_context_data(**kwargs)
        context['T_title'] = 'Feeds'
        return context

# add new memories.
class FeedCreateView(LoginRequiredMixin, CreateView):
    model = VirtualMemories
    template_name = 'Users_feeds/add_feed.html'
    fields = ['Add_tag', 'Add_note', 'Add_file']

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FeedCreateView, self).get_context_data(**kwargs)
        context['T_title'] = 'FeedCreate'
        return context

# update memory
class FeedUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VirtualMemories
    template_name = 'Users_feeds/add_feed.html'
    fields = ['Add_tag', 'Add_note', 'Add_file']

    def test_func(self):
        feed = self.get_object()
        if self.request.user.profile == feed.author:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(FeedUpdateView, self).get_context_data(**kwargs)
        context['T_title'] = 'FeedUpdate'
        return context


# memory delete view.
class FeedDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VirtualMemories
    template_name = 'main/posts_confirm_delete.html'

    def get_success_url(self):
        return reverse('feeds')

    def test_func(self):
        feed = self.get_object()
        if self.request.user.profile == feed.author:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(FeedDeleteView, self).get_context_data(**kwargs)
        context['T_title'] = 'FeedDelete'
        return context


# Like function to identify if user is already liked the post or not
@login_required
def FeedLikeView(request, pk):
    feed = get_object_or_404(VirtualMemories, id=request.POST.get('feed_id'))

    if feed.feed_likes.filter(id=request.user.id).exists():
        feed.feed_likes.remove(request.user)
        messages.success(request, f'unliked')
    else:
        feed.feed_likes.add(request.user)
        messages.success(request, f'liked')

    return HttpResponseRedirect(reverse('feed_comments', kwargs={'pk': pk}))


# all comment of individual feed
class CommentsView(ListView):
    model = Comment
    context_object_name = 'Comments'
    template_name = 'Users_feeds/comments.html'
    ordering = ['-comment_date']

    def get_queryset(self):
        feed_id = get_object_or_404(VirtualMemories, id=self.kwargs.get('pk'))
        return Comment.objects.filter(parent_feed=feed_id).order_by('-comment_date')

    def get_context_data(self, **kwargs):
        feed = get_object_or_404(VirtualMemories, id=self.kwargs.get('pk'))
        context = super(CommentsView, self).get_context_data(**kwargs)
        context['feed'] = feed
        context['T_title'] = 'Comment(s)'
        return context


# all reply of individual comment
class ReplyView(ListView):
    model = ReplyComment
    context_object_name = 'replies'
    template_name = 'Users_feeds/replies.html'
    ordering = ['-comment_reply_date']

    def get_queryset(self):
        comment_id = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        return ReplyComment.objects.filter(parent_comment=comment_id).order_by('-comment_reply_date')

    def get_context_data(self, **kwargs):
        comment = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        context = super(ReplyView, self).get_context_data(**kwargs)
        context['comment'] = comment
        context['T_title'] = 'Reply(s)'
        return context


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment']
    template_name = 'Users_feeds/Add_comments.html'

    def form_valid(self, form):
        form.instance.comment_person = self.request.user
        form.instance.parent_feed_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddComment, self).get_context_data(**kwargs)
        context['T_title'] = 'AddComment'
        return context


class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'Users_feeds/Add_comments.html'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.comment_person:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.comment_person = self.request.user
        # form.instance.parent_feed_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateComment, self).get_context_data(**kwargs)
        context['T_title'] = 'UpdateComment'
        return context


class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'main/posts_confirm_delete.html'

    def get_success_url(self):
        return reverse('feeds')

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.comment_person:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(DeleteComment, self).get_context_data(**kwargs)
        context['T_title'] = 'DeleteComment'
        return context


class AddReply(LoginRequiredMixin, CreateView):
    model = ReplyComment
    fields = ['reply']
    template_name = 'Users_feeds/Add_comments.html'

    def form_valid(self, form):
        form.instance.comment_reply_person = self.request.user
        form.instance.parent_comment_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddReply, self).get_context_data(**kwargs)
        context['T_title'] = 'AddReply'
        return context


class UpdateReply(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReplyComment
    fields = ['reply']
    template_name = 'Users_feeds/Add_comments.html'

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.comment_reply_person:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.comment_reply_person = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateReply, self).get_context_data(**kwargs)
        context['T_title'] = 'UpdateReply'
        return context


class DeleteReply(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ReplyComment
    template_name = 'main/posts_confirm_delete.html'

    def get_success_url(self):
        return reverse('feeds')

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.comment_reply_person:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(DeleteReply, self).get_context_data(**kwargs)
        context['T_title'] = 'DeleteReply'
        return context
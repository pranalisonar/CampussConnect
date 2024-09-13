from django.db.models import Count
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import FieldCategory, Field_Q, Field_Q_A
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# .....................import section closed.................................
@login_required
# Like function to identify if user is already liked the post or not
def FieldLikeView(request, pk):
    feed = get_object_or_404(FieldCategory, id=request.POST.get('field_id'))

    if feed.field_likes.filter(id=request.user.id).exists():
        feed.field_likes.remove(request.user)
        messages.success(request, f'interest removed')
    else:
        feed.field_likes.add(request.user)
        messages.success(request, f'interest added')

    return HttpResponseRedirect(reverse('field-category'))


class CategoryListView(LoginRequiredMixin, ListView):
    model = FieldCategory
    context_object_name = 'field_categories'
    queryset = FieldCategory.objects.annotate(like_count=Count('field_likes')).order_by('-like_count', '-id')
    template_name = 'Users_QA/field_categories.html'

    def get_context_data(self,**kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['T_title'] = 'FieldCategory'
        return context
# /-/-/-/--/-/-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/

# /-/-/-/--/-/-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/
# all question of selected field
class QuestionsView(ListView):
    model = Field_Q
    context_object_name = 'questions'
    template_name = 'Users_QA/field_q.html'
    total_len = 0

    def get_queryset(self):
        feed_id = get_object_or_404(FieldCategory, id=self.kwargs.get('pk'))
        self.total_len = len(Field_Q.objects.filter(parent_field=feed_id).order_by('-q_date'))
        return Field_Q.objects.filter(parent_field=feed_id).order_by('-q_date')

    def get_context_data(self, **kwargs):
        feed = get_object_or_404(FieldCategory, id=self.kwargs.get('pk'))
        context = super(QuestionsView, self).get_context_data(**kwargs)

        not_ans = len(Field_Q.objects.filter(parent_field=feed, answer=None).order_by('-q_date'))
        answered = len(Field_Q.objects.filter(parent_field=feed, answer__isnull=False).order_by('-q_date'))

        context['field'] = feed
        context['not_ans'] = not_ans
        context['answered'] = answered
        context['total'] = self.total_len
        context['T_title'] = 'Question(s)'
        return context


class AddQuestionToField(LoginRequiredMixin, CreateView):
    model = Field_Q
    fields = ['question']
    template_name = 'Users_QA/add_question.html'

    def form_valid(self, form):
        form.instance.q_person = self.request.user
        form.instance.parent_field_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(AddQuestionToField, self).get_context_data(**kwargs)
        context['T_title'] = 'AddQuestionToField'
        return context

@login_required
def search_question(request, pk):
    if request.method == 'POST':
        searched = request.POST['Q_search']
        posts = Field_Q.objects.filter(parent_field=pk, question__icontains=searched)
        return render(request, 'Users_QA/search_question.html', {'searches': searched, 'search_results': posts, 'T_title': 'SearchQuestion'})
    else:
        return reverse('field-questions', kwargs={'pk': pk})


@login_required
def QuestionLike(request, pk):
    q = get_object_or_404(Field_Q, id=request.POST.get('question_id'))

    if q.q_likes.filter(id=request.user.id).exists():
        q.q_likes.remove(request.user)
        messages.success(request, f'like removed')
    else:
        q.q_likes.add(request.user)
        messages.success(request, f'liked')

    return HttpResponseRedirect(reverse('field-questions', kwargs={'pk': q.parent_field.id}))


class UpdateQuestion(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Field_Q
    fields = ['question']
    template_name = 'Users_QA/add_question.html'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.q_person:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.q_person = self.request.user
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(UpdateQuestion, self).get_context_data(**kwargs)
        context['T_title'] = 'UpdateQuestion'
        return context


class DeleteQuestion(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Field_Q
    template_name = 'User_Blogs/posts_confirm_delete.html'

    def get_success_url(self):
        return reverse('field-category')

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.q_person:
            return True
        else:
            return False

    def get_context_data(self,**kwargs):
        context = super(DeleteQuestion, self).get_context_data(**kwargs)
        context['T_title'] = 'DeleteQuestion'
        return context
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# /-/-/-/--/-/-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/
# all ans of selected question
class QuestionsAnsView(ListView):
    model = Field_Q_A
    context_object_name = 'answers'
    template_name = 'Users_QA/q_a.html'

    def get_queryset(self):
        question = get_object_or_404(Field_Q, id=self.kwargs.get('pk'))
        return Field_Q_A.objects.filter(parent_q=question.id).order_by('-a_date')

    def get_context_data(self, **kwargs):
        feed = get_object_or_404(Field_Q, id=self.kwargs.get('pk'))
        context = super(QuestionsAnsView, self).get_context_data(**kwargs)
        context['question'] = feed
        context['T_title'] = 'Q_answer(S)'
        return context


class AddAnsToQuestion(LoginRequiredMixin, CreateView):
    model = Field_Q_A
    fields = ['answer']
    template_name = 'Users_QA/add_question.html'

    def form_valid(self, form):
        form.instance.a_person = self.request.user
        form.instance.parent_q_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(AddAnsToQuestion, self).get_context_data(**kwargs)
        context['T_title'] = 'AddAnsToQuestion'
        return context


@login_required
def AnsLike(request, pk):
    ans = get_object_or_404(Field_Q_A, id=request.POST.get('ans_id'))

    if ans.a_likes.filter(id=request.user.id).exists():
        ans.a_likes.remove(request.user)
        messages.success(request, f'vot removed')
    else:
        ans.a_likes.add(request.user)
        messages.success(request, f'voted')

    return HttpResponseRedirect(reverse('questions-ans', kwargs={'pk': ans.parent_q.id}))


class UpdateAns(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Field_Q_A
    fields = ['answer']
    template_name = 'Users_QA/add_question.html'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.a_person:
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.a_person = self.request.user
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(UpdateAns, self).get_context_data(**kwargs)
        context['T_title'] = 'UpdateAns'
        return context


class DeleteAns(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Field_Q_A
    template_name = 'main/posts_confirm_delete.html'

    def test_func(self):
        ans = self.get_object()
        if self.request.user == ans.a_person:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('field-category')

    def get_context_data(self,**kwargs):
        context = super(DeleteAns, self).get_context_data(**kwargs)
        context['T_title'] = 'DeleteAns'
        return context
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# /-/-/-/--/-/-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-//-/-/-/-/-/-/-/-/-//-/-/-/-/-/-/
class NotAnsweredQuestion(ListView):
    model = Field_Q
    context_object_name = 'questions'
    template_name = 'Users_QA/exp.html'

    def get_queryset(self):
        feed_id = get_object_or_404(FieldCategory, id=self.kwargs.get('pk'))
        return Field_Q.objects.filter(parent_field=feed_id, answer=None).order_by('-q_date')

    def get_context_data(self,**kwargs):
        context = super(NotAnsweredQuestion, self).get_context_data(**kwargs)
        context['T_title'] = 'NotAnsweredQuestion'
        return context


class AnsweredQuestion(ListView):
    model = Field_Q
    context_object_name = 'questions'
    template_name = 'Users_QA/exp.html'

    def get_queryset(self):
        feed_id = get_object_or_404(FieldCategory, id=self.kwargs.get('pk'))
        return Field_Q.objects.filter(parent_field=feed_id, answer__isnull=False).order_by('-q_date')

    def get_context_data(self,**kwargs):
        context = super(AnsweredQuestion, self).get_context_data(**kwargs)
        context['T_title'] = 'AnsweredQuestion'
        return context
# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/
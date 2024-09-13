# Create your views here.
from django.shortcuts import HttpResponse, Http404, render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from .models import QuestionPapers
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os


class QuestionPaperListView(ListView):
    model = QuestionPapers
    template_name = 'Question_papers/AllQuestionPapers.html'
    context_object_name = 'AllQuestionPapers'
    ordering = ['-Upload_date']

    def get_context_data(self, **kwargs):
        context = super(QuestionPaperListView, self).get_context_data(**kwargs)
        context['T_title'] = 'QuestionPaper(s)'
        return context


@login_required
def download_question_paper(request, pk):
    qp = get_object_or_404(QuestionPapers, id=pk)
    path = qp.Question_paper.path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def search_QP(request):
    if request.method == 'POST':
        searched = request.POST['Search_question_paper']
        question_papers = QuestionPapers.objects.filter(
            Q(Subject_name__icontains=searched) | Q(Exam_pattern__icontains=searched)
            | Q(Exam_Month__icontains=searched) | Q(Exam_Year__icontains=searched) | Q(Class_year__icontains=searched))
        return render(request, 'Question_papers/search_result_QP.html',
                      {'searches': searched, 'search_results': question_papers, 'T_title': 'Search_QP'})
    else:
        return render(request, 'Question_papers/AllQuestionPapers.html')
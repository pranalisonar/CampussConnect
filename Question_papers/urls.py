from django.urls import path
from .views import QuestionPaperListView, search_QP, download_question_paper

urlpatterns = [
    path('all/', QuestionPaperListView.as_view(), name='question_paper'),
    path('search-result/', search_QP, name='search_question_paper'),
    path('download/question-paper/<int:pk>', download_question_paper, name='question_paper_download'),
]
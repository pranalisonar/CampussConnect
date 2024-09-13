from django.urls import path
from .views import (CategoryListView, FieldLikeView, QuestionsView,QuestionLike, QuestionsAnsView,
                    AnsLike, AddQuestionToField, search_question,AddAnsToQuestion, UpdateQuestion,
                    DeleteQuestion, UpdateAns, DeleteAns, NotAnsweredQuestion, AnsweredQuestion)


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name="field-category"),
    path('field/<int:pk>/like', FieldLikeView, name='like_field'),

    path('field/<int:pk>/questions', QuestionsView.as_view(), name='field-questions'),
    path('field-ask-question/<int:pk>/', AddQuestionToField.as_view(), name='ask_question'),
    path('question/<int:pk>/like', QuestionLike, name='questions-like'),
    path('field-question/<int:pk>/search', search_question, name='questions-search'),
    path('field-question/<int:pk>/update', UpdateQuestion.as_view(), name='questions-update'),
    path('field-question/<int:pk>/delete', DeleteQuestion.as_view(), name='questions-delete'),

    path('question/<int:pk>/ans', QuestionsAnsView.as_view(), name='questions-ans'),
    path('field-add-question/<int:pk>/ans', AddAnsToQuestion.as_view(), name='add-question-ans'),
    path('field-question/<int:pk>/ans-update', UpdateAns.as_view(), name='update-question-ans'),
    path('field-question/<int:pk>/ans-delete', DeleteAns.as_view(), name='delete-question-ans'),
    path('ans/<int:pk>/vot', AnsLike, name='ans-like'),

    path('NotAnswered/<int:pk>', NotAnsweredQuestion.as_view(), name='exp'),
    path('Answered/<int:pk>', AnsweredQuestion.as_view(), name='ans'),
]
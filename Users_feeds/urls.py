from django.urls import path
from . import views

urlpatterns = [
    path('feeds/', views.FeedsListView.as_view(), name="feeds"),
    path('feeds/new-memory', views.FeedCreateView.as_view(), name="add_feed"),
    path('feeds/update/<int:pk>/memory', views.FeedUpdateView.as_view(), name="update_feed"),
    path('feeds/delete/<int:pk>/memory', views.FeedDeleteView.as_view(), name="delete_feed"),

    path('feeds/<int:pk>/like/', views.FeedLikeView, name='like_feed'),

    path('memory/<int:pk>/comments/', views.CommentsView.as_view(), name='feed_comments'),
    path('memory/new-comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
    path('memory/update-comment/<int:pk>', views.UpdateComment.as_view(), name='Update_comment'),
    path('memory/delete-comment/<int:pk>', views.DeleteComment.as_view(), name='Delete_comment'),

    path('memory/comment/<int:pk>/reply', views.ReplyView.as_view(), name='reply_comment'),
    path('memory/new-comment-reply/<int:pk>', views.AddReply.as_view(), name='add_reply'),
    path('memory/update-comment-reply/<int:pk>', views.UpdateReply.as_view(), name='update_reply'),
    path('memory/delete-comment-reply/<int:pk>', views.DeleteReply.as_view(), name='delete_reply'),
]
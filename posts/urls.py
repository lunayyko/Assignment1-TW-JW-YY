from django.urls import path
from .views      import PostListCreateView, CommentView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("/<int:post_id>/comments", CommentView.as_view())
]
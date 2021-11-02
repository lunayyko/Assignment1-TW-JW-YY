from django.urls import path
from .views      import PostListCreateView, PostRetrieveDeleteEditView, CommentView, CommentModifyView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path('/<int:post_id>', PostRetrieveDeleteEditView.as_view()),
    path("/<int:post_id>/comments", CommentView.as_view()),
    path("/<int:post_id>/comments/<int:comment_id>", CommentModifyView.as_view())
]
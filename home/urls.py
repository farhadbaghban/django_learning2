from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("post/<int:user_id>/", views.UserPostsView.as_view(), name="User_Posts"),
    path(
        "post/<int:post_id>/<slug:post_slug>",
        views.UserPostView.as_view(),
        name="User_Post",
    ),
    path(
        "post/delete/<int:post_id>/", views.PostDeleteView.as_view(), name="Post_Delete"
    ),
    path(
        "post/update/<int:post_id>/", views.PostUpdateView.as_view(), name="Post_Update"
    ),
    path("post/create/", views.PostCreateView.as_view(), name="Post_Create"),
    path(
        "comment/reply/<int:comment_id>/",
        views.CommentReplyView.as_view(),
        name="Comment_Reply",
    ),
    path("post/like/<int:post_id>/", views.UserLikeView.as_view(), name="post_like"),
]

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
]

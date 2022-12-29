from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="User_Registration"),
    path("login/", views.UserLoginView.as_view(), name="User_Login"),
    path("logout/", views.UserLogoutView.as_view(), name="User_Logout"),
    path(
        "profile/<int:user_id>/", views.UserProfileView.as_view(), name="User_Profile"
    ),
    path("reset/", views.UserPasswordResetView.as_view(), name="reset_password"),
    path(
        "reset/done/",
        views.UserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "confirm/<uidb64>/<token>/",
        views.UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "confirm/complete",
        views.UserPasswordResetCompleteView.as_view(),
        name="password_reset_completes",
    ),
    path("follow/<int:user_id>/", views.UserFollowView.as_view(), name="user_follow"),
    path(
        "unfollow/<int:user_id>/",
        views.UserUnfollowView.as_view(),
        name="user_unfollow",
    ),
    path("edit_user/", views.EditUserView.as_view(), name="edit_user"),
]

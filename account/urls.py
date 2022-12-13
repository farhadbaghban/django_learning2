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
]

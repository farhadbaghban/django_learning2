from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="Registration")
]

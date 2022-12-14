from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_class = "account/registeration.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password1"])
            messages.success(request, "Your registered SuccessFully", "success")
            return redirect("home:index")
        else:
            messages.error(request, "Enter Valid Data", "warning")
            return render(request, self.template_class, {"form": form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_class = "account/Login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "You Are Loged SuccessFully", "success")
                return redirect("home:index")
            messages.error(request, "username or password is Wrong", "warning")
        return render(request, self.template_class, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You are Logged out SuccessFully", "success")
        return redirect("home:index")


class UserProfileView(LoginRequiredMixin, View):
    template_class = "account/profile.html"

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, self.template_class, {"user": user, "posts": posts})

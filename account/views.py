from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from .models import Relation


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

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

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
                if self.next:
                    return redirect(self.next)
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
        exist_relation = False
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            exist_relation = True
        return render(
            request,
            self.template_class,
            {"user": user, "posts": posts, "exist_relation": exist_relation},
        )


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserFollowView(LoginRequiredMixin, View):
    template_class = "account:User_Profile"

    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(pk=kwargs["user_id"])
        self.user_logined = User.objects.get(pk=request.user.id)
        self.relation = Relation.objects.filter(
            from_user=self.user_logined, to_user=self.user_instance
        )
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.user_instance == self.user_logined:
            messages.error(request, "You Can't Follow your self", "danger")
            return redirect(
                self.template_class,
                self.user_instance.id,
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        if self.relation.exists():
            messages.error(request, "You Can't follow againg this User", "danger")
        else:
            Relation.objects.create(
                from_user=self.user_logined, to_user=self.user_instance
            )
            messages.success(
                request,
                f"You Are Followed {self.user_instance.username}   SuccessFully",
                "success",
            )
        return redirect(
            self.template_class,
            self.user_instance.id,
        )


class UserUnfollowView(LoginRequiredMixin, View):
    template_class = "account:User_Profile"

    def setup(self, request, *args, **kwargs):
        self.user_instance = User.objects.get(pk=kwargs["user_id"])
        self.user_logined = User.objects.get(pk=request.user.id)
        self.relation = Relation.objects.filter(
            from_user=self.user_logined, to_user=self.user_instance
        )
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.user_instance == self.user_logined:
            messages.error(request, "You Can't UnFollow your self", "danger")
            return redirect(
                self.template_class,
                self.user_instance.id,
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        if self.relation.exists():
            self.relation.delete()
            messages.success(
                request, f"You Unfollowe {self.user_instance}  SuccessFully", "success"
            )
        else:
            messages.error(
                request,
                f"You can't Unfollow {self.user_instance}.Becuse You Are Not Followed Him",
                "danger",
            )
        return redirect(
            self.template_class,
            self.user_instance.id,
        )

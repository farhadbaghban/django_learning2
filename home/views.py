from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Post
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {"posts": posts})


class UserPostsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, "home/userposts.html", {"posts": posts})


class UserPostView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.filter(pk=post_id, slug=post_slug)
        return render(request, "home/userposts.html", {"posts": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, "Post Deleted SuccessFully", "success")
        else:
            messages.error(request, "You Can't Delete This Post", "danger")
        return redirect("home:index")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_class = "home/update.html"

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "You Can't Update This Post", "danger")
            return redirect("home:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.slug = slugify(form.cleaned_data["body"][:30])
            new_form.save()
            messages.success(request, "Post Updated SuccessFully", "success")
            return redirect("home:User_Post", post.id, post.slug)

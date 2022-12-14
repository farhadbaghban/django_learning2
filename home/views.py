from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Post


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
    def get(self, request, slug):
        post = Post.objects.filter(slug=slug)
        return render(request, "home/userposts.html", {"posts": post})

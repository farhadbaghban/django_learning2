from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Post, Comment, Vote
from django.contrib import messages
from .forms import (
    PostCreateUpdateForm,
    CommentCreateForm,
    CommentReplyForm,
    PostSearchForm,
)
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get("search"):
            posts = posts.filter(body__contains=request.GET.get("search"))
        return render(
            request, "home/index.html", {"posts": posts, "form": self.form_class}
        )


class UserPostsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, "home/userposts.html", {"posts": posts})


class UserPostView(View):
    form_class = CommentCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(
            pk=kwargs["post_id"], slug=kwargs["post_slug"]
        )
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        comments = self.post_instance.pcomments.all()
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(
            request.user
        ):
            can_like = True
        return render(
            request,
            "home/userpost.html",
            {
                "post": self.post_instance,
                "form": form,
                "comments": comments,
                "can_like": can_like,
            },
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "Your Comment added successFully. ", "success")
            return redirect(
                "home:User_Post", self.post_instance.id, self.post_instance.slug
            )


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
    form_class = PostCreateUpdateForm
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

    def get(self, request, post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_class, {"form": form})

    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.slug = slugify(form.cleaned_data["body"][:30])
            new_form.save()
            messages.success(request, "Post Updated SuccessFully", "success")
            return redirect("home:User_Post", post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_class = "home/create.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.slug = slugify(form.cleaned_data["body"][:30])
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Your Post Created SuccessFully", "success")
            return redirect("home:User_Post", new_form.id, new_form.slug)
            # return redirect("account:User_Profile", request.user.id)


class CommentReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm
    template_class = "home/comment_reply.html"

    def setup(self, request, *args, **kwargs):
        self.comment_instance = Comment.objects.get(pk=kwargs["comment_id"])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        replies = self.comment_instance.rcomments.all()
        return render(
            request,
            self.template_class,
            {"form": form, "comment": self.comment_instance, "replies": replies},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.is_reply = True
            new_reply.user = self.comment_instance.user
            new_reply.post = self.comment_instance.post
            new_reply.reply = self.comment_instance
            new_reply.save()
            messages.success(request, "Your Reply addded successFully", "success")
            return redirect("home:Comment_Reply", self.comment_instance.id)


class UserLikeView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.liked_before = Vote.objects.filter(
            user=request.user, post=self.post_instance
        )
        if self.liked_before:
            messages.error(request, "you liked Before", "danger")
            return redirect(
                "home:User_Post", self.post_instance.id, self.post_instance.slug
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        liked = Vote(user=request.user, post=self.post_instance)
        liked.is_post = True
        liked.save()
        messages.success(request, "You liked", "success")
        return redirect(
            "home:User_Post",
            self.post_instance.id,
            self.post_instance.slug,
        )

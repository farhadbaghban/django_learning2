from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("home:User_Post", args=(self.id, self.slug))

    def liked_count(self):
        return self.pvotes.count()

    def user_can_like(self, user):
        can_like = user.uvotes.filter(post=self)
        if can_like.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomments")
    reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="rcomments",
        blank=True,
        null=True,
    )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}  -  {self.body[:30]}"

    def comment_count(self):
        return self.cvotes.count()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvotes")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="pvotes", blank=True, null=True
    )
    is_post = models.BooleanField(default=False)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="cvotes", blank=True, null=True
    )
    is_comment = models.BooleanField(default=False)

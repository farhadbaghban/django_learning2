from django.contrib import admin
from .models import Post, Comment, Vote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "updated")
    search_fields = ("slug",)
    list_filter = ("updated", "created")
    prepopulated_fields = {"slug": ("body",)}
    raw_id_fields = ("user",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "is_reply", "created")
    raw_id_fields = ("user", "post", "reply")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "is_post", "post", "is_comment", "comment")
    raw_id_fields = ("user", "post", "comment")

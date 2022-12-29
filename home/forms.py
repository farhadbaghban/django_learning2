from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body",)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"class": "col-md-4 text-white bg-dark"})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"class": "col-md-4 text-white bg-dark"})
        }


class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

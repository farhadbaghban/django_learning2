from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages


class UserRegistrationView(View):
    form_class = RegistrationForm
    template_class = "account/registeration.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_class, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password"])
            messages.success(request, "Your registered SuccessFully", "success")
            return redirect("home:index")
        else:
            messages.error(request, "Enter Valid Data", "warning")
            return render(request, self.template_class, {"form": form})

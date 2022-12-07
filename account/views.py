from django.shortcuts import render
from .forms import RegistrationForm
from django.views import View


class UserRegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "account/registeration.html", {"form": form})

    def post(self, request):
        pass

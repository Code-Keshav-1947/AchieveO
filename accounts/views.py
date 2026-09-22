from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/dashboard")

    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs.update({"class": "form-control"})

    return render(request, "accounts/login.html", {"form": form})

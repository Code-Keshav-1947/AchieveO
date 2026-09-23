from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OwnerProfileForm
from owners.utils import get_current_owner


@login_required
def profile_view(request):
    owner = get_current_owner(request.user)

    if request.method == "POST":
        form = OwnerProfileForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            messages.success(request, "Business profile updated successfully!")
            return redirect("profile")
    else:
        form = OwnerProfileForm(instance=owner)

    return render(
        request,
        "owners/profile.html",
        {
            "form": form,
            "owner": owner,
            "active_tab": "profile",
        },
    )

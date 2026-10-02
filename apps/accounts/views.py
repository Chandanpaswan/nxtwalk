from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from .forms import RegistrationForm, UserDetailsForm, UserProfileForm
from .models import UserProfile


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, "Your NXTWALK account is ready.")
        return redirect("accounts:profile")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile_record, _ = UserProfile.objects.get_or_create(user=request.user)
    user_form = UserDetailsForm(request.POST or None, instance=request.user, prefix="user")
    profile_form = UserProfileForm(request.POST or None, instance=profile_record, prefix="profile")
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        with transaction.atomic():
            user_form.save()
            profile_form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"user_form": user_form, "profile_form": profile_form})
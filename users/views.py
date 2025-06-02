# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile instance
            UserProfile.objects.create(user=user) # Default role is 'patient'
            login(request, user)
            messages.success(request, 'Registration successful! Welcome.')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'page_title': 'Register'})

@login_required
def profile_view(request):
    # UserProfile is automatically created via signal or can be fetched
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        # This case should ideally be handled by creating a profile on user creation
        UserProfile.objects.create(user=request.user)
        user_profile = request.user.profile

    context = {
        'user_profile': user_profile,
        'page_title': 'My Profile'
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit_view(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)
        user_profile = request.user.profile

    if request.method == 'POST':
        # User form for basic user details (first_name, last_name, email)
        # For simplicity, let's focus on profile form here. You can add a UserChangeForm too.
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'profile_form': profile_form,
        'page_title': 'Edit Profile'
    }
    return render(request, 'users/profile_edit.html', context)
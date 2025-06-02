# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'core/home.html', {'page_title': 'Welcome to FeminaCare AI'})

@login_required
def dashboard_view(request):
    context = {
        'page_title': 'Your Dashboard',
        'user_profile': request.user.profile # Assuming profile is created on user creation
    }
    # Add logic to fetch data specific to the user role for the dashboard
    if request.user.profile.is_admin:
        # Fetch admin specific data
        pass
    elif request.user.profile.is_patient:
        # Fetch patient specific data
        pass
    return render(request, 'core/dashboard.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm
from .models import Profile


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

@login_required
def profile_list(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_profiles')
        selected_ids = [pid for pid in selected_ids if pid != str(request.user.profile.id)]
        Profile.objects.filter(id__in=selected_ids).delete()
        return redirect('profile_list')

    profiles = Profile.objects.select_related('user')
    return render(request, 'profile_list.html', {'profiles': profiles})
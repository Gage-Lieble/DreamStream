from django.shortcuts import render
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect

# Login/Signup functions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def signup(request):
   # Displays before form input
    if request.method == 'GET':
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'user_dreamstream/signup.html', context)
    # Creates a new User
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                password = form.cleaned_data['password'],
                email = form.cleaned_data['email'],
            )
        return HttpResponseRedirect(reverse('dream_users:signup'))
def user_login(request):
    if request.method == 'GET':
        context = {'log_form': LoginForm()}
        return render(request, 'user_dreamstream/login.html', context)
    elif request.method == 'POST':
        log_form = LoginForm(request.POST)
        if log_form.is_valid():
            password = log_form.cleaned_data['password'] # Clears any empty spaces and removes them
            user =  authenticate(request, username=log_form.cleaned_data['username'], password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('dream_users:profile'))
            else:
                log_form.add_error('username', 'Invalid email or password')
                return render(request, 'user_dreamstream/login.html', {'log_form': log_form})
            

@login_required
def profile(request):
    return render(request, 'user_dreamstream/profile.html')

    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('dream_users:login'))


# def user_logout(request)